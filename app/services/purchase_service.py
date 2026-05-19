from app.repositories.purchase_repo import create_purchase
from app.services.stock_service import stock_in


def process_purchase(db, data):
    total_amount = data.unit_price * data.quantity

    purchase_data = {
        "vendor_id": data.vendor_id,
        "product_id": data.product_id,
        "quantity": data.quantity,
        "unit_price": data.unit_price,
        "total_amount": total_amount,
        "status": data.status or "pending",
        "purchase_officer_id": data.purchase_officer_id,
    }

    stock_in(db, data.product_id, data.quantity)
    return create_purchase(db, purchase_data)
