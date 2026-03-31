import pdfplumber
import docx

def load_pdf(file_path: str)->str:
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def load_txt(file_path: str) -> str:
    with open(file_path,'r',encoding='utf-8') as file:
        return file.read()

def load_docs(file_path: str):
    doc = docx.Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)
    
def load_document(file_path: str) -> str:
    file_path = str(file_path)
    if file_path.endswith('.pdf'):
        return load_pdf(file_path)
    elif file_path.endswith('.txt'):
        return load_txt(file_path)
    else:
        return load_docs(file_path)

# Note: PDF processing runs sunchronously. For production, blocking operations should run in a separate thread or process to avoid blocking the main event loop.
# For example, you can use `asyncio.to_thread` to run the PDF loading function in a separate thread:
# Or, if you are using a web framework like FastAPI, you can use `run_in_threadpool` from `starlette.concurrency` to run the blocking function in a thread pool.
# another one, ThreadPoolExecutor(max_workers) from concurrent.futures import ThreadPoolExecutor
# ThreadPoolExecutor can be used to manage a pool of threads and execute tasks asynchronously. You can submit the PDF loading function to the executor and get a Future object that represents the result of the operation. This allows you to run multiple PDF loading tasks concurrently without blocking the main thread.
# TreadPoolExecutor -> more control, production grade
# ru_in_treadpool -> simpler, FastAPI buit-in, same result