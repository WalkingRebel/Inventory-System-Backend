from typing import List, cast
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseOut
from app.services.purchase_service import process_purchase
from app.dependencies import get_current_user
from app.models.user import User
from app.models.purchase import PurchaseOrder
from app.utils.api_guard import guarded
from app.utils.pagination import paginate

router = APIRouter()


@router.post(
    "/",
    response_model=PurchaseOut,
    summary="Create a purchase order",
    description="Records a purchase transaction and increases stock for the purchased product.",
)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["purchase"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="purchase_order",
        operation="CREATE",
        actor_user_id=current_user_id,
        entity_id_from_result=lambda r: (
            str(getattr(r, "id", None)) if getattr(r, "id", None) is not None else None
        ),
        before_payload=data.model_dump(),
        after_payload=None,
        action=lambda: process_purchase(db, data),
        request=request,
    )


@router.get(
    "/",
    response_model=List[PurchaseOut],
    summary="List purchase orders",
    description="Returns all recorded purchase orders.",
)
def list_purchases(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["purchase"]),
):
    return paginate(db.query(PurchaseOrder), page, limit)


@router.get(
    "/{purchase_id}",
    response_model=PurchaseOut,
    summary="Get a purchase order",
    description="Returns a single purchase order by ID.",
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["purchase"]),
):
    purchase = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase