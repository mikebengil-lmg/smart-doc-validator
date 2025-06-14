from typing import Optional

from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.schemas.base import FileExtractorRequest, default_model
from app.core.llm import run_document_analysis

router = APIRouter()

@router.post("/smart_document_classify", response_class=JSONResponse)
async def smart_document_classify(request: FileExtractorRequest):
    response = await run_document_analysis(request)
    return JSONResponse(content=response)


# test endpoint for testing file upload classification
@router.post("/smart_document_classify_test", response_class=JSONResponse)
async def smart_document_classify_test(
    file: UploadFile,
    # infer from file.content_type
    model: Optional[str] = Form(None)
):
    file_bytes = await file.read()
    import base64
    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    content_type_map = {
        "image/jpeg": "jpeg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "text/plain": "txt",
        "text/csv": "csv"
    }
    content_type = content_type_map.get(file.content_type, "jpeg")  # default fallback

    model_to_use = model or default_model

    request_data = FileExtractorRequest(
        file_base64=file_base64,
        file_type=content_type,
        model=model_to_use
    )

    response = await run_document_analysis(request_data)
    return JSONResponse(content=response)