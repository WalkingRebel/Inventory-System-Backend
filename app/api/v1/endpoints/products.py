from typing import List, cast
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import create_product_service, list_products_service
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.utils.api_guard import guarded
from app.utils.pagination import paginate

router = APIRouter()


@router.post(
    "/",
    response_model=ProductOut,
    summary="Create a product",
    description="Creates a new product entry in the catalog. Intended for admin users.",
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["products"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="products",
        operation="CREATE",
        actor_user_id=current_user_id,
        entity_id_from_result=lambda r: (
            str(getattr(r, "id", None)) if getattr(r, "id", None) is not None else None
        ),
        before_payload=data.model_dump(),
        after_payload=None,
        action=lambda: create_product_service(db, data),
        request=request,
    )


@router.get(
    "/",
    response_model=List[ProductOut],
    summary="List products",
    description="Returns all products in the catalog.",
)
def list_products(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["products"]),
):
    return paginate(db.query(Product), page, limit)


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Get a product",
    description="Returns a single product by ID.",
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["products"]),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Update a product",
    description="Updates fields on an existing product.",
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["products"]),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete(
    "/{product_id}",
    summary="Delete a product",
    description="Permanently deletes a product from the catalog.",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["products"]),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}