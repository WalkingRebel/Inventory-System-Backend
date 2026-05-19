from app.repositories.stock_repo import log_stock
from app.services.inventory_service import update_inventory


def stock_in(db, product_id, qty):
    update_inventory(db, product_id, qty)
    log_stock(db, product_id, qty, "In")


def stock_out(db, product_id, qty):
    update_inventory(db, product_id, -qty)
    log_stock(db, product_id, qty, "Out")
