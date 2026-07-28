import os
import requests

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.utils import save_image

app = FastAPI(title="My Upload Service")


@app.get("/")
def root():
    return {
        "service": "Upload Service",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    allowed_extensions = [".jpg", ".jpeg", ".png"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG files are allowed."
        )

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    file.file.seek(0)

    # Save image
    saved_filename, original_filename = save_image(file)

    # Call converter service
    try:
        
        CONVERTER_URL = os.getenv("CONVERTER_URL")

        response = requests.post(
            CONVERTER_URL,
            json={
                "filename": saved_filename
            },
            timeout=30
        )

    except requests.exceptions.RequestException:

        raise HTTPException(
            status_code=500,
            detail="Converter Service is currently unavailable."
        )

    if response.status_code != 200:

        raise HTTPException(
            status_code=500,
            detail="Image conversion failed."
        )

    pdf_filename = response.json()["pdf_name"]

    # IMPORTANT: use outputs (plural)
    pdf_path = f"/shared/outputs/{pdf_filename}"

    if not os.path.exists(pdf_path):

        raise HTTPException(
            status_code=404,
            detail="Converted PDF not found."
        )

    # User downloads original filename.pdf
    download_name = os.path.splitext(original_filename)[0] + ".pdf"

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=download_name
    )