import json
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
    return JSONResponse(content=json.loads(result))