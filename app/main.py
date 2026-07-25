from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.converter import (
    validate_file,
    convert_image_to_pdf
)

app = FastAPI(
    title="Cloud Native Document Platform",
    version="1.0.0"
)

# Exposes /metrics automatically
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    return {
        "project": "Cloud Native Document Platform",
        "message": "Image to PDF Conversion API"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/version")
def version():
    return {
        "version": app.version,
        "environment": "local"
    }


@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    try:
        validate_file(file.filename)

        pdf = convert_image_to_pdf(file.file)

        pdf_name = file.filename.rsplit(".", 1)[0] + ".pdf"

        return StreamingResponse(
            pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{pdf_name}"'
            },
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Image conversion failed."
        )