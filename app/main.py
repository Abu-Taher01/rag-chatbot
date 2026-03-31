from typing import Optional
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi import Body
import psycopg
from psycopg.rows import dict_row
from . import models, chat, schemas
from .rag import rag_schemas
from .rag.rag_service import file_processing
from .database import engine, get_db
from sqlalchemy.orm import Session
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# session_id = "default_session"  # This is a placeholder. In a real application, you would generate or manage session IDs properly.

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "RAG chatbot", 
              version = "1.0.0", 
              description = "A simple RAG chatbot API built with FastAPI and SQLAlchemy")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Chatbot API!"}

@app.post("/chat", response_model=schemas.ChatResponse)
def chat_endpoint(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    answer = chat.chat(db, request.session_id, request.question, request.use_rag)
    # return schemas.ChatResponse(answer=answer)
    # return {"session_id": request.session_id, "answer": answer}
    return schemas.ChatResponse(
        session_id = request.session_id,
        answer = answer
    )

@app.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    history = chat.get_conversation_history(db, session_id)
    return {"history": history}

@app.post("/upload/{session_id}", response_model = rag_schemas.UploadResponse)
async def upload_document(file: UploadFile = File(...), session_id: str = None):
    logging.info(f"Received file: {file.filename}, content type: {file.content_type}")
    if not session_id or len(session_id.strip()) < 5:
        raise HTTPException(status_code=400, detail="Valid session_id is required")
    
    logging.info(f"Upload request for session {session_id} - file: {file.filename}") 
    return await file_processing(file, session_id)