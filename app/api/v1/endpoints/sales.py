from typing import cast
from fastapi import APIRouter, Depends, Request, Security, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.sales import SalesCreate, SalesOut
from app.services.sales_service import process_sale
from app.dependencies import get_current_user
from app.models.user import User
from app.utils.api_guard import guarded

from app.models.sales import SalesOrder
from typing import List

router = APIRouter()


@router.post(
    "/",
    response_model=SalesOut,
    summary="Create a sales order",
    description="Records a sales transaction and is intended to decrease stock for the sold product.",
)
def create_sale(
    data: SalesCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["sales"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="sales_order",
        operation="CREATE",
        actor_user_id=current_user_id,
        entity_id_from_result=lambda r: (
            str(getattr(r, "id", None)) if getattr(r, "id", None) is not None else None
        ),
        before_payload=data.model_dump(),
        after_payload=None,
        action=lambda: process_sale(db, data),
        request=request,
    )

@router.get(
    "/",
    response_model=List[SalesOut],
    summary="List sales orders",
    description="Returns all recorded sales orders.",
)
def list_sales(
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["sales"]),
):
    return db.query(SalesOrder).all()

@router.get(
    "/{sale_id}",
    response_model=SalesOut,
    summary="Get a sales order",
    description="Returns a single sales order by ID.",
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["sales"]),
):
    sale = db.query(SalesOrder).filter(SalesOrder.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale