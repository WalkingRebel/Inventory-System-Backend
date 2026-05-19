from app.models.stock_transaction import StockTransaction


def log_stock(db, product_id, qty, type_):
    tx = StockTransaction(product_id=product_id, quantity=qty, type=type_)
    db.add(tx)
    db.commit()
