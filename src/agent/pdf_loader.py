import fitz  # PyMuPDF
import io

def extract_text_from_pdf(file):
    """Extract text from a PDF file (handles both path and Streamlit uploads)."""
    # If it's an uploaded file (Streamlit), read bytes and open from memory
    if hasattr(file, "read"):
        pdf_bytes = file.read()
        doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    else:
        # Otherwise assume it's a local file path
        doc = fitz.open(file)

    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text
