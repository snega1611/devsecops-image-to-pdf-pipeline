import io

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def create_test_image():

    image = Image.new("RGB", (100, 100), color="red")

    image_bytes = io.BytesIO()

    image.save(image_bytes, format="PNG")

    image_bytes.seek(0)

    return image_bytes


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "Healthy"


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_upload_invalid_extension():

    response = client.post(
        "/upload",
        files={
            "file": ("test.txt", b"hello", "text/plain")
        }
    )

    assert response.status_code == 400


def test_upload_empty_file():

    response = client.post(
        "/upload",
        files={
            "file": ("empty.png", b"", "image/png")
        }
    )

    assert response.status_code == 400