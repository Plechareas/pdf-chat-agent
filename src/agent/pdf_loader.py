import fitz

def extract_text_from_pdf(path:str)-> str:
    """"Extracts all text from a PDF file."""
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
        doc.close
        return text