from typing import List, cast
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.api_guard import guarded

router = APIRouter()


@router.post(
    "/",
    response_model=UserOut,
    summary="Create a user",
    description="Creates a new user record with a hashed password and assigned role.",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["users"]),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user with this email already exists."
        )

    def _action():
        db_user = User(
            email=user_in.email,
            name=user_in.name,
            role_id=user_in.role_id,
            password=hash_password(user_in.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    before_payload = user_in.model_dump()
    before_payload.pop("password", None)

    return guarded(
        db=db,
        table_name="users",
        operation="CREATE",
        actor_user_id=current_user_id,
        entity_id_from_result=lambda r: (
            str(getattr(r, "id", None)) if getattr(r, "id", None) is not None else None
        ),
        before_payload=before_payload,
        after_payload=None,
        action=_action,
        request=request,
    )


@router.get(
    "/",
    response_model=List[UserOut],
    summary="List all users",
    description="Returns all users. Requires users scope.",
)
def list_users(
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["users"]),
):
    return db.query(User).all()


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    description="Returns the profile of the currently authenticated user.",
)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None,
):
    current_user_id = cast(int, current_user.id)
    return guarded(
        db=db,
        table_name="users",
        operation="READ",
        actor_user_id=current_user_id,
        entity_id=str(current_user_id),
        before_payload=None,
        after_payload=None,
        action=lambda: current_user,
        request=request,
    )


@router.get(
    "/admin",
    summary="Check admin access",
    description="Confirms the current user has admin permissions.",
)
def admin_only(current_user: User = Security(get_current_user, scopes=["admin"])):
    return {"message": "Admin access granted"}


@router.put(
    "/{user_id}",
    response_model=UserOut,
    summary="Update a user",
    description="Updates name, password, or role of an existing user.",
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["users"]),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    summary="Delete a user",
    description="Permanently removes a user from the system.",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Security(get_current_user, scopes=["users"]),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}