import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TextChunker:
    def __init__(self,chunk_size:int = 800, chunk_overlap: int = 150, separators: List[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n","\n",". ","! ","? "," ",""]

        logger.info(f"Initialized TextChunker with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    
    def text_chunker(self, text: str) -> List[Dict[str,Any]]:
        if not text or not text.strip():
            logger.warning("Empty text for chunking")
            return []
        
        text=re.sub(r'\n\s*\n', '\n\n', text.strip())
        text=re.sub(r' +',' ', text)

        chunks= []
        cur_pos = end_pos = 0
        chunk_index =0

        while cur_pos<len(text):
            end_pos = cur_pos + self.chunk_size

            if end_pos < len(text):
                for sep in self.separators:
                    pos =text.rfind(sep, cur_pos, end_pos)
                    if pos != -1 and pos > cur_pos+50:
                        end_pos = pos + len(sep)
                        break
            
            chunk = text[cur_pos:end_pos].strip()

            if chunk:
                chunks.append(
                    {
                        "content" : chunk,
                        "chunk_index" : chunk_index,
                        "start_pos" : cur_pos,
                        "end_pos" :end_pos,
                        "length" :len(chunk)
                    }
                )
                chunk_index += 1
            
            if end_pos>=len(text):
                break;
        
            cur_pos = end_pos - self.chunk_overlap

            # print(f"{cur_pos} - {end_pos} - {len(text)}")
        
        logger.info(f"Created {len(chunks)} chunks from the document")
        return chunks
    
    def doc_chunker(self, text:str, filename: str = None) -> List[Dict[str,Any]]:
        """Chunker with Metadata"""

        base_chunks = self.text_chunker(text)
        for chunk in base_chunks:
            chunk["filename"] = filename
            chunk["metadata"] = {
                "filename": filename,
                "chunk_index": chunk["chunk_index"],
                "char_length": chunk["length"],
                "total_chunk" : len(base_chunks)
            }

        return base_chunks

# # ============== Simple usage example (for testing) ==============
# if __name__ == "__main__":
#     chunker = TextChunker(chunk_size=200, chunk_overlap=30)
    
#     test_text = """Machine learning is a field of artificial intelligence.
#     It allows computers to learn from data without being explicitly programmed.

#     Deep learning is a subset of machine learning that uses neural networks with many layers.
#     Transformers, introduced in 2017, revolutionized the field of NLP."""
    
#     chunks = chunker.doc_chunker(test_text, filename="test_text.txt")
    
#     for i, chunk in enumerate(chunks):
#         for key,value in chunk.items():
#             print(f"{key} -- {value}")
#         print('\n\n')
#     #     print(f"Chunk {i}: {len(chunk['content'])} chars")
#     #     print(chunk['content'][:200] + "...\n")
            



        
