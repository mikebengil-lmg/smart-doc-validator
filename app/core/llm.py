# app/core/llm.py
import base64
import json
from datetime import datetime, timezone
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import prompt_path, parse_model_input, init_chat_model, MAX_TOKENS, llm_cost

from docx import Document
import io
import csv

from app.schemas.base import default_model


async def run_document_analysis(request):
    mime_type_map = {
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "txt": "text/plain",
        "csv": "text/csv"
    }
    mime_type = mime_type_map.get(request.file_type.lower(), "application/octet-stream")

    # Handle supported text-based formats
    if request.file_type.lower() == "docx":
        docx_data = base64.b64decode(request.file_base64)
        doc = Document(io.BytesIO(docx_data))
        text_content = "\n".join(p.text for p in doc.paragraphs)
    elif request.file_type.lower() == "txt":
        text_content = base64.b64decode(request.file_base64).decode("utf-8")
    elif request.file_type.lower() == "csv":
        csv_data = base64.b64decode(request.file_base64).decode("utf-8")
        reader = csv.reader(io.StringIO(csv_data))
        text_content = "\n".join([", ".join(row) for row in reader])
    else:
        text_content = None

    file_prompt = []

    if text_content:
        file_prompt.append({"type": "text", "text": text_content})
    else:
        file_prompt.append({
            "type": "image",
            "source_type": "base64",
            "data": request.file_base64,
            "mime_type": mime_type,
        })

    with open(f"{prompt_path}/smart_classifier.md") as f:
        raw_prompt = f.read()

    today_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    instructions_prompt = raw_prompt.replace("{today}", today_str)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=instructions_prompt),
        HumanMessage(content=file_prompt)
    ])

    provider, model_id = parse_model_input(request.model or default_model)
    llm = init_chat_model(model_provider=provider, model=model_id, max_tokens=MAX_TOKENS)
    chain = prompt | llm

    # Pass the base64 data to the LLM input, key name can remain 'image_data' or you can rename to 'file_data' if needed
    response = await chain.ainvoke({"file_data": request.file_base64})

    response.usage_metadata = getattr(response, "usage_metadata", {})
    response.usage_metadata['total_cost'] = llm_cost(request.model, response.usage_metadata)
    response.usage_metadata['model'] = request.model or default_model

    # Parse the JSON string inside `response.content`
    try:
        parsed_content = json.loads(response.content)
    except Exception as ex:
        print(f"[WARNING] Failed to parse LLM response for file: {ex}")
        parsed_content = {
            "summary": "ignore this file, unable to classify properly",
            "fraud_risk": "high",
            "fraud_notes": "LLM could not parse a valid document from the input image. Possibly not a document or image is too distorted."
        }

    # Optionally, attach metadata if needed
    # parsed_content["_usage"] = response.usage_metadata

    return parsed_content

async def run_relationship_validation(request):
    from langchain.prompts import ChatPromptTemplate
    from langchain_core.messages import SystemMessage, HumanMessage
    from app.core.config import prompt_path, parse_model_input, init_chat_model, MAX_TOKENS

    prompt_text = open(f"{prompt_path}/batch_relationship_validator.md").read()
    system = SystemMessage(content=prompt_text)
    human = HumanMessage(content=json.dumps(request.dict(), indent=2))

    prompt = ChatPromptTemplate.from_messages([system, human])

    model_to_use = request.model or default_model
    provider, model_id = parse_model_input(model_to_use)
    llm = init_chat_model(model_provider=provider, model=model_id, max_tokens=MAX_TOKENS)

    chain = prompt | llm
    result = await chain.ainvoke({})

    return result.content
