from app.models.purchase import PurchaseOrder


def create_purchase(db, data: dict):
    purchase = PurchaseOrder(**data)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase
