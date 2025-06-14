from pydantic import BaseModel

default_model = "bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0"

class FileExtractorRequest(BaseModel):
    file_base64: str
    file_type: str  # e.g. "jpeg", "png", "pdf", "docx", "txt", "csv"
    model:str = default_model      # e.g. "gpt-4", "gpt-3.5-turbo"
