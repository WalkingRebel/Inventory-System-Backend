from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "notreal@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401

def test_login_missing_fields():
    response = client.post("/api/v1/auth/login", data={})
    assert response.status_code == 422