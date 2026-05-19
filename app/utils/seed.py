from app.core.database import SessionLocal
from app.models.role import Role

ROLE_MAP = {
    1: "admin",
    2: "purchase",
    3: "sales",
    4: "customer",
    5: "vendor",
}


def seed_roles():
    db = SessionLocal()

    for role_id, role_name in ROLE_MAP.items():
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            role.name = role_name
        else:
            db.add(Role(id=role_id, name=role_name))
    db.commit()
    db.close()
    print("Roles seeded successfully")


if __name__ == "__main__":
    seed_roles()

from app.core.security import hash_password
from app.models.user import User

def seed_admin():
    db = SessionLocal()
    existing = db.query(User).filter(User.email == "admin@admin.com").first()
    if not existing:
        admin = User(
            name="Admin",
            email="admin@admin.com",
            password=hash_password("admin123"),
            role_id=1,
        )
        db.add(admin)
        db.commit()
        print("Admin user created: admin@admin.com / admin123")
    else:
        print("Admin already exists")
    db.close()

if __name__ == "__main__":
    seed_roles()
    seed_admin()