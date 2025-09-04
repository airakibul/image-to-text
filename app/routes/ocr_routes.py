from fastapi import APIRouter, UploadFile, File
from app.schemas.ocr_schema import OCRResponse
from app.services.ocr_service import extract_text_from_image_bytes

router = APIRouter()

@router.post("/ocr", response_model=OCRResponse)
async def run_ocr(file: UploadFile = File(...)):
    # Read the uploaded file bytes
    file_bytes = await file.read()
    text = extract_text_from_image_bytes(file_bytes)
    return OCRResponse(extracted_text=text)
