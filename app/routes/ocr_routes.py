from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ocr_schema import OCRResponse
from app.services.ocr_service import extract_text

router = APIRouter()

@router.post("/ocr", response_model=OCRResponse)
async def run_ocr(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text(file_bytes, file.filename)
        return OCRResponse(extracted_text=text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
