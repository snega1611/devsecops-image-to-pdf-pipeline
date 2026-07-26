from fastapi import FastAPI

from app.models import ConvertRequest, ConvertResponse
from app.converter import convert_to_pdf

app = FastAPI(title="Converter Service")


@app.get("/")
def root():
    return {"service": "Converter Service"}


@app.get("/health")
def health():
    return {"status": "Healthy"}


@app.post("/convert", response_model=ConvertResponse)
def convert(request: ConvertRequest):

    pdf_name = convert_to_pdf(request.filename)

    return ConvertResponse(
        pdf_name=pdf_name,
        message="PDF created successfully."
    )