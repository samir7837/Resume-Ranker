import pdfplumber
import docx
import os

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    except Exception as e:
        print(f"PDF extraction error for {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"DOCX extraction error for {file_path}: {e}")
        return ""

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    print(f"Attempting to extract: {file_path}, ext: {ext}")
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print("Unsupported file type.")
        return ""