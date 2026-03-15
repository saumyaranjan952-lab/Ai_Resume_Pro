import PyPDF2
import docx
import io

def extract_text_from_pdf(file):
    """Extract text from uploaded PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file):
    """Extract text from uploaded DOCX file."""
    text = ""
    try:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text(file, file_type):
    """Wrapper function to extract text based on file type."""
    if file_type == "application/pdf":
        return extract_text_from_pdf(file)
    elif "wordprocessingml.document" in file_type:
        return extract_text_from_docx(file)
    else:
        return ""
