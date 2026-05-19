from app.repositories.inventory_repo import list_inventory, update_stock


def update_inventory(db, product_id, quantity):
    return update_stock(db, product_id, quantity)


def list_inventory_service(db):
    return list_inventory(db)
