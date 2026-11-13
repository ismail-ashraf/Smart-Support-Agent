from typing import List, Optional
from pydantic import BaseModel


# Ingest Schemas
class IngestResponse(BaseModel):
    chunks_added: int
    doc_id: str
    message: str


# RAG Query Schemas
class QueryRequest(BaseModel):
    question: str
    chat_id: Optional[str] = None
    language: Optional[str] = "ar"


class Passage(BaseModel):
    text: str
    source: str
    section: str
    score: float


class QueryResponse(BaseModel):
    passages: List[Passage]
    top_score: float


# Intent Classification Schemas
class IntentRequest(BaseModel):
    message_text: str


class IntentResponse(BaseModel):
    intent: str  # faq, lead, complaint, other
    confidence: float


# Lead Extraction Schemas
class LeadMessage(BaseModel):
    role: str
    content: str


class LeadExtractRequest(BaseModel):
    messages: List[LeadMessage]


class LeadExtractResponse(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    need: Optional[str] = None
    budget: Optional[str] = None
    score: float = 0.0
    missing_fields: List[str] = []