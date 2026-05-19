from sqlalchemy import func
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.purchase import PurchaseOrder
from app.models.sales import SalesOrder


def get_basic_report(db):
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_inventory_units = (
        db.query(func.coalesce(func.sum(Inventory.quantity), 0)).scalar() or 0
    )
    total_purchase_amount = (
        db.query(func.coalesce(func.sum(PurchaseOrder.total_amount), 0)).scalar() or 0
    )
    total_sales_amount = (
        db.query(func.coalesce(func.sum(SalesOrder.total_amount), 0)).scalar() or 0
    )

    return {
        "total_products": total_products,
        "total_inventory_units": total_inventory_units,
        "total_purchase_amount": total_purchase_amount,
        "total_sales_amount": total_sales_amount,
    }
