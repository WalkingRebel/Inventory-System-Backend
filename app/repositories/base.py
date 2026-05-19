from __future__ import annotations
from typing import Any, TypeVar
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


def add_commit_refresh(db: Session, obj: ModelT) -> ModelT:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def commit(db: Session) -> None:
    db.commit()


def delete_commit(db: Session, obj: Any) -> None:
    db.delete(obj)
    db.commit()


def refresh(db: Session, obj: Any) -> None:
    db.refresh(obj)
