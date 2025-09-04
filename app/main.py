from fastapi import FastAPI
from app.routes import ocr_routes

app = FastAPI(title="HARMONI-AI OCR API")

app.include_router(ocr_routes.router, prefix="/api")
