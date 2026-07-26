from pydantic import BaseModel


class ConvertRequest(BaseModel):
    filename: str


class ConvertResponse(BaseModel):
    pdf_name: str
    message: str