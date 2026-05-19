from app.models.product import Product


def create_product(db, data):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db):
    return db.query(Product).all()
