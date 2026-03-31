import logging
from pathlib import Path
from fastapi import HTTPException, UploadFile, status

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def validate_file(file: UploadFile):
    if not file.filename.lower().endswith(('.txt', '.pdf', '.docx')):
        logger.warning(f"Unsupported file type: {file.filename}")
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail="Unsupported file type. Only .txt, .pdf, and .docx are allowed."
        )
    
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        logger.warning(f"File size exceeds limit: {file.filename} ({len(content)} bytes)")
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the maximum limit of 10 MB."
        )
    
    logger.info(f"File {file.filename} passed validation checks.")
    return content
    # if file.size > MAX_FILE_SIZE:

async def save_file(file: UploadFile, content: bytes) -> str:
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_path = UPLOAD_DIR/file.filename
    try:
        logger.info(f"Saving file to: {file_path}")
        with open(file_path, "wb") as f:
            f.write(content)
            # shutil.copyfileobj(file.file, f) is better for large files because it reads and writes the file in chunks, which can help to reduce memory usage and improve performance. When you use f.write(content), it reads the entire file into memory before writing it to disk, which can be inefficient for large files and may lead to memory errors. On the other hand, shutil.copyfileobj(file.file, f) allows you to copy the file in smaller chunks, which can help to avoid memory issues and improve the overall efficiency of the file upload process.
    
    except Exception as e:
        logger.error(f"Error while saving the file: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while saving the file. Please try again later."
        )
    
    return file_path