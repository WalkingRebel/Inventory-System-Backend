from typing import cast
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

OAUTH_SCOPES = {
    "admin": "Full administrative access",
    "inventory:read": "Read inventory",
    "inventory:write": "Adjust inventory",
    "purchase": "Create/manage purchase orders",
    "sales": "Create/manage sales orders",
    "reports": "View reporting endpoints",
    "products": "Create/manage products",
    "users": "Create/manage users",
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    scopes=OAUTH_SCOPES,
)

ROLE_SCOPES_BY_ID: dict[int, set[str]] = {
    1: set(OAUTH_SCOPES.keys()),
    2: {"purchase", "inventory:read", "inventory:write"},
    3: {"sales", "inventory:read"},
    4: {"sales"},
    5: {"purchase"},
}


def _scopes_for_role(role_id: int | None) -> set[str]:
    if role_id is None:
        return set()
    return ROLE_SCOPES_BY_ID.get(int(role_id), set())


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    required = set(security_scopes.scopes or [])
    if required:
        allowed = _scopes_for_role(cast(int | None, user.role_id))
        missing = required - allowed
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scope(s): {', '.join(sorted(missing))}",
            )

    return user


def require_role(allowed_roles: list):
    normalized = set()
    for role in allowed_roles:
        try:
            normalized.add(int(role))
        except (ValueError, TypeError):
            continue

    def _checker(current_user: User = Depends(get_current_user)):
        if cast(int | None, current_user.role_id) not in normalized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return current_user

    return _checker


def require_scopes(scopes: list[str]):
    def _checker(current_user: User = Security(get_current_user, scopes=scopes)):
        return current_user

    return _checker
