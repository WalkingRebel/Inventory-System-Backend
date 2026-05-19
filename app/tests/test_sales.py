from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_sale_unauthenticated():
    response = client.post("/api/v1/sales/", json={
        "customer_id": 1,
        "product_id": 1,
        "unit_price": 10.0,
        "quantity": 1,
    })
    assert response.status_code == 401

def test_list_sales_unauthenticated():
    response = client.get("/api/v1/sales/")
    assert response.status_code == 401