import os
from pathlib import Path


BASE_DIR = Path(
    os.getenv("STORAGE_PATH", "./storage")
)

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_image(file):

    extension = Path(file.filename).suffix

    import uuid
    import shutil

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return unique_filename