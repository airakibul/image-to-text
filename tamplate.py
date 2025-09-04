import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    ".env",
    ".gitignore",
    "README.md",
    "requirements.txt",
    "app/__init__.py",
    "app/config.py",
    "app/main.py",
    "app/scheduler.py",
    "app/agents/__init__.py",
    "app/data/__init__.py",
    "app/data/sample_inputs/handwritten_note.jpg",
    "app/enum/__init__.py",
    "app/routes/__init__.py",
    "app/routes/ocr_routes.py",
    "app/schemas/__init__.py",
    "app/schemas/ocr_schema.py",
    "app/services/__init__.py",
    "app/services/ocr_service.py",
    "app/utils/__init__.py",
    "app/utils/image_utils.py",
    "python-sdk/__init__.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # For files
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        # If it's the .jpg file, just create an empty placeholder
        if filepath.suffix == ".jpg":
            with open(filepath, "wb") as f:
                pass
        else:
            with open(filepath, "w") as f:
                pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
