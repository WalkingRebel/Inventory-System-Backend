from fastapi import HTTPException
from app.repositories.sales_repo import create_sale
from app.repositories.inventory_repo import get_inventory_by_product
from app.services.stock_service import stock_out


def process_sale(db, data):
    inventory = get_inventory_by_product(db, data.product_id)
    if not inventory or inventory.quantity < data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    total_amount = data.unit_price * data.quantity

    sale_data = {
        "customer_id": data.customer_id,
        "product_id": data.product_id,
        "quantity": data.quantity,
        "unit_price": data.unit_price,
        "total_amount": total_amount,
        "status": data.status or "pending",
        "sales_officer_id": data.sales_officer_id,
    }

    stock_out(db, data.product_id, data.quantity)
    return create_sale(db, sale_data)
