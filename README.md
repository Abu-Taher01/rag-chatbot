# RAG Chatbot API

A full-featured Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, PostgreSQL, FAISS, and Groq LLM.

## Features

- Upload and process PDF, TXT, and DOCX documents
- Per-session document isolation (each user/session has separate FAISS index)
- Hybrid RAG with optional `use_rag` flag
- Persistent conversation history using PostgreSQL + SQLAlchemy
- Fast semantic search using Sentence-Transformers + FAISS
- Clean REST API with Swagger documentation

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Vector Store**: FAISS (per-session indexing)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: Groq (Llama-3.1-8B-Instant)
- **Document Processing**: pdfplumber, python-docx

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/{session_id}` | Upload document for a specific session |
| POST | `/chat` | Chat with RAG support |
| GET | `/history/{session_id}` | Get conversation history |

### Example Request - Chat

```json
{
  "session_id": "abd12345",
  "question": "What is the main topic discussed in the document?",
  "use_rag": true
}
```

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Abu-Taher01/rag-chatbot
cd rag-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env file with GROQ_API_KEY and PostgreSQL credentials
```
GROQ_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost/rag_chatbot
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

### 5. Test via Swagger UI
Navigate to `http://127.0.0.1:8000/docs`

## 📁 Project Architecture

```
rag-chatbot/
├── main.py
├── chat.py
├── models.py
├── schemas.py
├── database.py
├── rag/
│   ├── document_loader.py
│   ├── text_chunker.py
│   ├── vector_store.py
│   ├── rag_service.py
│   ├── rag_pipeline.py
│   └── rag_schemas.py
├── faiss_index/           # Per-session vector stores
├── uploads/               # Temporary upload folder
├── .env
└── requirements.txt
```

## Key Implementations

- Built complete RAG pipeline from scratch (without LangChain)
- Implemented per-session FAISS indexing for user data isolation
- Hybrid RAG with relevance checking
- Clean separation between document processing and chat logic

## Future Improvements

- Background processing for large document uploads
- Memory optimization for large ebooks
- Migration to PGVector for better scalability
- Docker + deployment on Render

---

**Author**: Abu-Taher01  (ABDULLAH AL MAMUN)
**License**: MIT
