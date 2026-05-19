from app.models.sales import SalesOrder


def create_sale(db, data: dict):
    sale = SalesOrder(**data)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
