from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_adjust_inventory_unauthenticated():
    response = client.post("/api/v1/inventory/", json={
        "product_id": 1,
        "quantity": 10,
    })
    assert response.status_code == 401

def test_get_inventory_unauthenticated():
    response = client.get("/api/v1/inventory/1")
    assert response.status_code == 401