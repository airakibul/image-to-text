from fastapi import APIRouter
from app.schemas.ocr_schema import OCRRequest, OCRResponse
from app.services.ocr_service import extract_text_from_image

router = APIRouter()

@router.post("/ocr", response_model=OCRResponse)
def run_ocr(request: OCRRequest):
    text = extract_text_from_image(request.image_path)
    return OCRResponse(extracted_text=text)
