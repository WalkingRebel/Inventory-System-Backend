from app.models.inventory import Inventory


def get_inventory_by_product(db, product_id):
    return db.query(Inventory).filter_by(product_id=product_id).first()


def list_inventory(db):
    return db.query(Inventory).all()


def update_stock(db, product_id, quantity):
    inv = get_inventory_by_product(db, product_id)

    if not inv:
        inv = Inventory(product_id=product_id, quantity=0)
        db.add(inv)

    inv.quantity += quantity
    db.commit()
    db.refresh(inv)
    return inv
