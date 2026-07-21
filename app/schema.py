# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

class DocumentClassification(BaseModel):
    doc_type: str = Field(description="e.g. invoice, receipt, id_card, contract, resume")
    confidence: float = Field(description="0-1 confidence score")

class ExtractedField(BaseModel):
    field_name: str
    value: str

class ExtractionResult(BaseModel):
    doc_type: str
    fields: List[ExtractedField]
    raw_notes: Optional[str] = None

class ValidatedResult(BaseModel):
    doc_type: str
    fields: List[ExtractedField]
    is_valid: bool
    issues: Optional[List[str]] = None