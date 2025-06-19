import json
import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.validation import BatchValidationRequest
from app.core.llm import run_relationship_validation

router = APIRouter()

@router.post("/validate_batch", response_class=JSONResponse)
async def validate_batch(request: BatchValidationRequest):
    result = await run_relationship_validation(request)
    return JSONResponse(content=result)

@router.post("/validate_batch_formatted", response_class=JSONResponse)
async def validate_batch_formatted(request: BatchValidationRequest):
    result = await run_relationship_validation(request)

    if not result or not isinstance(result, str):
        return JSONResponse(status_code=500, content={"error": "Empty or invalid LLM response"})

    # Remove markdown-style code blocks if present
    cleaned = re.sub(r"^```json\s*|\s*```$", "", result.strip())

    try:
        parsed = json.loads(cleaned)
        return JSONResponse(content=parsed)
    except Exception as ex:
        return JSONResponse(status_code=500, content={
            "error": f"Failed to parse LLM response as JSON",
            "exception": str(ex),
            "raw": result
        })