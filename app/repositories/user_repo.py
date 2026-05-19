from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_oauth_user(db: Session, user_data, role_id: int):
    user = User(
        name=user_data["name"],
        email=user_data["email"],
        oauth_provider="google",
        oauth_id=user_data.get("sub"),
        role_id=role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
