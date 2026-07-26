from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "Healthy"


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_convert_missing_file():

    response = client.post(
        "/convert",
        json={
            "filename": "does-not-exist.png"
        }
    )

    assert response.status_code == 404