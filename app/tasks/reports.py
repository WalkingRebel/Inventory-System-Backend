from sqlalchemy import func
from app.core.database import SessionLocal
from app.core.celery_app import celery_app
from app.models import Product, SalesOrder


@celery_app.task(name="reports.sales_summary")
def sales_summary():
    db = SessionLocal()
    try:
        rows = (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.coalesce(func.sum(SalesOrder.total_amount), 0).label("total_sales"),
            )
            .outerjoin(SalesOrder, SalesOrder.product_id == Product.id)
            .group_by(Product.id, Product.name)
            .order_by(Product.name.asc())
            .all()
        )

        return [
            {
                "product_id": r.product_id,
                "product_name": r.product_name,
                "total_sales": float(r.total_sales or 0),
            }
            for r in rows
        ]
    finally:
        db.close()