from pydantic import BaseModel
from typing import List, Dict, Any

class UploadResponse(BaseModel):
    message : str
    filename : str
    total_chunks : int
    total_characters : int
    chunks: List[Dict[str,Any]]

    class Config:
        from_attributes = True

class RAGRequest(BaseModel):
    question: str

class RAGResponse(BaseModel):
    answer: str
    chunks: list[str]
    scores: list[float]
    class Config:
        from_attributes = True