from app.models.user import User


def get_user(db):
    return db.query(User).all()
