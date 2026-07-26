from pathlib import Path

UPLOAD_DIR = Path("/shared/uploads")
OUTPUT_DIR = Path("/shared/outputs")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)