from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    session_id : str = Field(..., min_length = 5, max_length = 20, description="Unique identifier for the chat session")
    question : str = Field(..., min_length = 1, max_length = 2000, description="The user's question to the chatbot")
    use_rag: Optional[bool] = Field(True, description="Whether to use RAG (document retrieval) or not. Default is True.")
    
class ChatResponse(BaseModel):
    session_id :str
    answer: str

class msg_create(BaseModel):
    session_id : str
    role : str
    content : str

class ConversationHistory(BaseModel):
    role: str
    content : str
    created_at : datetime

    class Config:
        from_attributes = True