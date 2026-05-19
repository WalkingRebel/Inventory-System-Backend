from app.repositories.user_repo import get_user_by_email, create_oauth_user
from app.core.security import verify_password, create_access_token


def login_user_service(db, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not user.password:
        return None

    if not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email, "role": user.role_id})
    return {"access_token": token, "token_type": "bearer"}


def handle_oauth_user(db, user_data: dict):
    user = get_user_by_email(db, user_data["email"])
    if not user:
        user = create_oauth_user(db, user_data, role_id=2)
    return user
