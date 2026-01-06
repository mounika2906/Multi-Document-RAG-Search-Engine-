from typing import Dict, Any, List
from pydantic import BaseModel

class Document(BaseModel):
    source_id: str
    source_type: str  # pdf, wikipedia, web
    title: str
    content: str
    metadata: Dict[str, Any]

class DocumentChunk(BaseModel):
    source_id: str
    source_type: str
    title: str
    content: str
    chunk_index: int
    metadata: Dict[str, Any]

class WebSearchResult(BaseModel):
    title: str
    content: str
    url: str
    metadata: Dict[str, Any]

class AnswerSource(BaseModel):
    source_type: str
    title: str
    citation: str
    content: str