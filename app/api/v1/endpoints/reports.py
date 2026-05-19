from typing import cast
from fastapi import APIRouter, Depends, Request, Security
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.report_service import get_basic_report
from app.utils.api_guard import guarded

router = APIRouter()


@router.get(
    "/",
    summary="Get summary reports",
    description="Returns high-level reporting data for products, inventory, purchases, and sales. Intended for admin users.",
)
def reports(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["reports"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="reports",
        operation="READ",
        actor_user_id=current_user_id,
        before_payload=None,
        after_payload=None,
        action=lambda: get_basic_report(db),
        request=request,
    )
