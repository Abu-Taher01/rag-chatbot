import logging
from fastapi import HTTPException, status
from groq import Groq
from sqlalchemy.orm import Session
from .models import Conversation
from .rag.rag_pipeline import RAGPipeline
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

rag_pipeline = RAGPipeline()

def get_conversation_history(db: Session, session_id: str):
    messages = (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.created_at)
        .all()
    )
    return [{"role" : msg.role, "content": msg.content} for msg in messages]

def save_messages(db: Session, session_id: str, role: str, content: str):
    message = Conversation(
        session_id = session_id,
        role = role,
        content = content
    )
    db.add(message)
    db.commit()


SYSTEM_PROMPT = (
    " You are a math genius. You are passionate about solving complex mathematical problems and sharing your insights with others."
    " You have a deep understanding of various mathematical concepts and theories, and you enjoy exploring new ideas and approaches to problem-solving."
    " Your goal is to help others understand and appreciate the beauty of mathematics, and you are always eager to share your knowledge and expertise with those who are interested in learning more."
)


def chat(db: Session, session_id: str, question: str, use_rag: bool = True) -> str:
    logger.info(f"Received question for session {session_id}: {question}")
    
    # Conversation memory
    conversation_history = get_conversation_history(db, session_id)[-10:]

    save_messages(db, session_id=session_id, role="user", content=question)

    if use_rag:
        user_content = rag_pipeline.process_query(session_id, question)
    else:
        user_content = question
    
    logger.info(f"Processing question with{'' if use_rag==True else 'out'} RAG for session {session_id}: {question}")
    
    try :
        # calling LLM to get the answer
        models = ["llama-3.3-70b-versatile", "gemini-1.5-pro", "gemini-2.0-pro", "llama-3.1-8b-instant", "openai/gpt-oss-120b",]
        
        response = client.chat.completions.create(
            model = models[4],
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ] 
            + conversation_history + [
                {
                    "role": "user", 
                    "content": user_content
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error while calling the LLM: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "The AI service is currently unavailable. Please try again later."
        )

    save_messages(db, session_id=session_id, role="assistant", content=answer)
    logger.info(f"Generated answer for session {session_id}: {answer}")

    return answer