from fastapi import UploadFile, HTTPException, status
from typing import List, Dict
from pathlib import Path
from .document_loader import load_document
from .rag_schemas import UploadResponse 
from .file_handler import validate_file, save_file
from .text_chunker import TextChunker
from .vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)

vector_store = VectorStore()

async def file_processing(file: UploadFile, session_id: str) -> UploadResponse:
    if not session_id:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Valid session_id is required."
        )
    
    # validate file
    content = await validate_file(file)
    # save the file
    file_path = await save_file(file, content)

    # loading the document and convert into text and Chunking 
    try:
        text = load_document(file_path)

        # Chunking The Text
        chunker = TextChunker(chunk_size=700, chunk_overlap=200)
        chunks = chunker.doc_chunker(text, file.filename)

        logger.info(f"{file.filename} chunked into {len(chunks)}")

        vector_store.add_doc(session_id=session_id, new_chunks=chunks)

        logger.info(f"Document '{file.filename}' successfully indexed for session {session_id}")
        
        return UploadResponse(
            message =  "Document processed and chunked successfully",
            filename = file.filename,
            total_chunks = len(chunks),
            total_characters =  len(text),
            chunks =  chunks[:3]
        )
    
    except ValueError as e:
        # failed to parse, Delete it
        Path(file_path).unlink(missing_ok=True)
        logger.error(f"Failed to parse document: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    
    finally:
        try:
            Path(file_path).unlink(missing_ok=True)
            logger.info(f"Deleted processed file: {file_path}")

        except Exception as e:
            logger.warning(f"could not delete file {file_path} : {e}")