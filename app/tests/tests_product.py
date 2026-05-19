from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_products_list():
    response = client.get("/api/v1/products/")
    assert response.status_code == 401
