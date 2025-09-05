from app.config import client
import base64
from io import BytesIO
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from docx import Document
from PIL import Image

# --- Existing image OCR ---
def extract_text_from_image_bytes(file_bytes: bytes) -> str:
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Extract the text from this handwritten note."},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ]
        }]
    )
    return response.output_text

# --- PDF text & image extraction ---
def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text = ""
    # 1. Extract typed text
    pdf_reader = PdfReader(BytesIO(file_bytes))
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    # 2. Extract images using PyMuPDF
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in pdf_doc:
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_bytes = base_image["image"]
            try:
                ocr_text = extract_text_from_image_bytes(image_bytes)
                text += f"\n{ocr_text}"
            except:
                pass  # ignore if OCR fails
    return text

# --- DOCX text & image extraction ---
def extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    text = ""
    doc = Document(BytesIO(file_bytes))
    for p in doc.paragraphs:
        text += p.text + "\n"

    # Extract images from docx
    for rel in doc.part._rels:
        rel = doc.part._rels[rel]
        if "image" in rel.target_ref:
            image_bytes = rel.target_part.blob
            try:
                ocr_text = extract_text_from_image_bytes(image_bytes)
                text += f"\n{ocr_text}"
            except:
                pass
    return text

# --- Unified extraction ---
def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.split('.')[-1].lower()
    if ext in ["jpg", "jpeg", "png"]:
        return extract_text_from_image_bytes(file_bytes)
    elif ext == "pdf":
        return extract_text_from_pdf_bytes(file_bytes)
    elif ext in ["doc", "docx"]:
        return extract_text_from_docx_bytes(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
