from pathlib import Path
from PIL import Image
from fastapi import HTTPException

from app.utils import UPLOAD_DIR, OUTPUT_DIR


def convert_to_pdf(filename: str):

    image_path = UPLOAD_DIR / filename

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Image not found."
        )

    pdf_name = Path(filename).stem + ".pdf"

    pdf_path = OUTPUT_DIR / pdf_name

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(pdf_path, "PDF")

    return pdf_name