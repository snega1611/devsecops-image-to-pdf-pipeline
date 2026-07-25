from io import BytesIO
from PIL import Image


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def validate_file(filename: str):
    if "." not in filename:
        raise ValueError("Invalid file name.")

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only JPG, JPEG and PNG files are supported.")


def convert_image_to_pdf(file) -> BytesIO:
    """
    Converts an uploaded image into a PDF and returns
    an in-memory PDF file.
    """

    image = Image.open(file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    pdf_buffer = BytesIO()

    image.save(pdf_buffer, format="PDF")

    pdf_buffer.seek(0)

    return pdf_buffer