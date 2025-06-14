from pydantic import BaseModel
from typing import List, Optional, Literal

from app.schemas.base import default_model


class DocumentSummary(BaseModel):
    document_index: Optional[int] = None  # Useful for traceability
    type: Optional[str] = None  # e.g., Passport, Payslip
    name: Optional[str] = None  # Subject of the document
    dob: Optional[str] = None  # Date of birth if present
    id_number: Optional[str] = None  # Passport ID, employee ID, etc.
    expiry: Optional[str] = None  # Expiry or validity end
    country: Optional[str] = None  # Country of issuance
    issuer: Optional[str] = None  # E.g., "Department of Foreign Affairs" or "ABC Corp"
    document_date: Optional[str] = None  # E.g., payslip period or issue date
    related_person: Optional[str] = None  # E.g., parent/child/spouse if document is not about client
    document_context: Optional[str] = None  # E.g., "Identification", "Financial"
    confidence: Optional[float] = None
    confidence_label: Optional[Literal["High", "Reasonable", "Weak"]] = None
    fraud_risk: Optional[Literal["low", "medium", "high"]] = None  # AI-assessed fraud risk
    fraud_notes: Optional[str] = None  # Any suspicious patterns or findings
    summary: Optional[str] = None  # Plain text summary of document

class ClientLookup(BaseModel):
    client_name: str
    dob: Optional[str] = None
    gender: Optional[str] = None

class BatchValidationRequest(BaseModel):
    documents: List[DocumentSummary]
    clients: List[ClientLookup]
    enum_filetypes: List[str]  # optional in prompt
    model:str = default_model  # e.g. "gpt-4", "gpt-4o"