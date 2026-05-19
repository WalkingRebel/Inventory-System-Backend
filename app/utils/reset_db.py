import os
from urllib.parse import urlparse

from app.core.config import settings
from app.core.database import Base, engine
from app.models import audit_logs  # noqa: F401
from app.utils.seed import seed_roles


def _sqlite_file_from_url(database_url: str) -> str | None:
    parsed = urlparse(database_url)
    if parsed.scheme != "sqlite":
        return None

    path = parsed.path or ""
    # sqlite:///./inventory.db => path "/./inventory.db" (relative)
    # sqlite:////abs/path.db => path "//abs/path.db" (absolute)
    stripped = path.lstrip("/")
    if path.startswith("//"):
        return "/" + stripped
    return stripped


def reset_db() -> None:
    db_path = _sqlite_file_from_url(settings.DATABASE_URL)
    if not db_path:
        raise RuntimeError(
            f"reset_db only supports sqlite DATABASE_URL. Got: {settings.DATABASE_URL}"
        )

    if os.path.exists(db_path):
        os.remove(db_path)

    Base.metadata.create_all(bind=engine)
    seed_roles()

    print(f"Database reset complete: {db_path}")


if __name__ == "__main__":
    reset_db()
