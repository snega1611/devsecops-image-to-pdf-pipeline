import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("/shared/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_image(file: UploadFile):

    extension = os.path.splitext(file.filename)[1]

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return both filenames
    return unique_filename, file.filename