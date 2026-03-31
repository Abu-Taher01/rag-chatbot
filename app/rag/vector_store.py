import faiss
import numpy as np
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorStore:
    
    def __init__(self, embed_model:str="sentence-transformers/all-MiniLM-L6-v2", dimension:int=384):
        self.embedding_model_name = embed_model
        self.dimension = dimension
        
        logger.info(f"Loading embedding model: {embed_model}")

        self.embedder = SentenceTransformer(embed_model)
        # self.index : Optional[faiss.Index] = None
        # self.chunks : List[Dict[str,Any]] = []

        logger.info(f"Vector store initialized successfully with {embed_model}")
    

    def get_index_path(self, session_id:str) -> Path:
        path = Path(f"faiss_index/session_{session_id}")
        path.mkdir(parents=True, exist_ok=True)
        return path


    # load previously saved faiss index and chunks pkl from disk
    def _load_index(self, session_id:str):
        index_path = self.get_index_path(session_id)
        index_file = index_path/"index.faiss"
        chunks_file = index_path/"chunks.pkl"
        
        if index_file.exists() and chunks_file.exists():
            try:
                index = faiss.read_index(str(index_file))
                with open(chunks_file,"rb") as f:
                    chunks = pickle.load(f)
                
                logger.info(f"Loaded faiss index with {len(chunks)} chunks for {session_id}")
                return index, chunks
            
            except Exception as e:
                logger.error(f"Failed to load faiss index for {session_id}: {e}")

        else:
            logger.info(f"No existing Faiss index found for {session_id}.")
        
        return None, []


    # adding documnet chunks to the vector store
    def add_doc(self, session_id: str, new_chunks : List[Dict[str,Any]]) -> None:
        if not new_chunks:
            logger.warning(f"NO chunks provided to add.")
            return
        
        index_path = self.get_index_path(session_id)
        index, existing_chunks = self._load_index(session_id)
        
        text = [chunk['content'] for chunk in new_chunks]

        logger.info(f"Generating embeddings for {len(new_chunks)} chunks with {self.embedding_model_name}")
        embeddings = self.embedder.encode(text, convert_to_numpy=True, batch_size=32)

        if index is None:
            index = faiss.IndexFlatL2(self.dimension)
            logger.info(f"Created new Faiss IndexFlatL2 with {self.dimension} dimensions")

        index.add(embeddings.astype(np.float32))
        existing_chunks.extend(new_chunks)

        # saving 
        try:
            faiss.write_index(index, str(index_path/"index.faiss"))

            with open(index_path/"chunks.pkl", "wb") as f:
                pickle.dump(existing_chunks, f)

            logger.info(f"Saved Faiss index and chunks to {index_path}")
        
        except Exception as e:
            logger.error(f"Failed to save Faiss index and chunks to {index_path}: {e}")


    # Search for top chunks for given query
    def search(self, session_id:str , query: str, top_k: int=5) -> List[Dict[str,Any]]:

        index, chunks = self._load_index(session_id)
        if index is None or len(chunks)==0:
            logger.warning(f"Vector store of {session_id} is empty.")
            return []

        embed_query = self.embedder.encode([query],convert_to_numpy=True)
        distances, indices = index.search(embed_query.astype(np.float32),top_k)

        result = []
        for i,idx in enumerate(indices[0]):
            if 0<=idx and idx<len(chunks):
                chunk = chunks[int(idx)].copy()
                chunk['score'] = float(distances[0][i])
                result.append(chunk)
        
        logger.info(f"Recived top {len(distances[0])} chunks")
        return result
    

    def get_total_chunks(self,session_id:str) -> int:
        _, chunks = self._load_index(session_id)
        return len(chunks)