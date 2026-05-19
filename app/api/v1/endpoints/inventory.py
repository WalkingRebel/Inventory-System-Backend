from typing import List, cast
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.inventory import InventoryOut, InventoryUpdate
from app.services.inventory_service import list_inventory_service, update_inventory
from app.repositories.inventory_repo import get_inventory_by_product
from app.dependencies import get_current_user
from app.models.user import User
from app.utils.api_guard import guarded
from app.utils.pagination import paginate
from app.models.inventory import Inventory

router = APIRouter()


@router.get(
    "/",
    response_model=List[InventoryOut],
    summary="List inventory",
    description="Returns the current inventory rows.",
)
def list_inventory(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["inventory:read"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="inventory",
        operation="READ",
        actor_user_id=current_user_id,
        before_payload=None,
        after_payload=None,
        action=lambda: paginate(db.query(Inventory), page, limit),
        request=request,
    )


@router.get(
    "/{product_id}",
    response_model=InventoryOut,
    summary="Get inventory by product",
    description="Returns the inventory record for a specific product.",
)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["inventory:read"]),
):
    inv = get_inventory_by_product(db, product_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found for this product")
    return inv


@router.post(
    "/",
    summary="Adjust inventory",
    description="Adjusts inventory quantity for a product.",
)
def update_stock(
    data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["inventory:write"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="inventory",
        operation="UPDATE",
        actor_user_id=current_user_id,
        entity_id=str(data.product_id),
        before_payload=data.model_dump(),
        after_payload=None,
        action=lambda: update_inventory(db, data.product_id, data.quantity),
        request=request,
    )