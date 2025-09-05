import mimetypes
import io
from PyPDF2 import PdfReader
from docx import Document
import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Try text extraction from PDF.
    If page has no text, fallback to OCR on page image.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text and len(page_text.strip()) > 20:
            texts.append(page_text.strip())
        else:
            # Fallback: render page to image, OCR
            pix = pdf_doc[i].get_pixmap()
            img_bytes = pix.tobytes("png")
            from app.services.ocr_service import extract_text_from_image_bytes
            texts.append(extract_text_from_image_bytes(img_bytes))

    return "\n".join(texts)

def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from docx.
    If no text, try OCR on embedded images.
    """
    doc = Document(io.BytesIO(file_bytes))
    texts = [p.text for p in doc.paragraphs if p.text.strip()]

    if texts:
        return "\n".join(texts)

    # Fallback: check for embedded images
    ocr_results = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            img_bytes = rel.target_part.blob
            from app.services.ocr_service import extract_text_from_image_bytes
            ocr_results.append(extract_text_from_image_bytes(img_bytes))

    return "\n".join(ocr_results)

def get_file_type(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"
