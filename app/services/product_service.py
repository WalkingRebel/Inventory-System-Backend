from app.repositories.product_repo import create_product, get_products


def create_product_service(db, data):
    return create_product(db, data)


def list_products_service(db):
    return get_products(db)
