import logging
from .vector_store import VectorStore
from typing import Any, List,Dict, Optional

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()

    def _build_context(self, retrived_chunks: List[Dict[str,Any]]) -> str:
        context = "Relevant information from the uploaded documents: \n"

        for i, chunk in enumerate(retrived_chunks, start=1):
            context += f"Chunk_{i} ---\n {chunk['content']}\n\n"

        return context.strip()

    def process_query(self, session_id:str, question:str) ->str:
        
        retrieved_chunks = self.vector_store.search(session_id,question,top_k=5)

        context = self._build_context(retrieved_chunks)

        user_content = f"Context from documents:\n{context} \n\n Question: {question} \n\n Answer the question based on the provided context. If the context does not contain relevant information, answer based on your general knowledge."

        return user_content