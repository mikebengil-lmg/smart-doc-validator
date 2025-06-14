from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import classify, validate

load_dotenv()  # Loads variables from .env into environment

app = FastAPI(title="Smart Document Validator", version="0.1")
app.include_router(classify.router, prefix="/api/v1")
app.include_router(validate.router, prefix="/api/v1")