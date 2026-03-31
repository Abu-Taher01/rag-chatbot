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