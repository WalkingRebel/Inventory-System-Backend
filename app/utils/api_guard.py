from collections.abc import Callable
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.services.audit_service import write_audit_log


def guarded(
    *,
    db: Session,
    table_name: str,
    operation: str,
    actor_user_id: int | None,
    entity_id: str | None = None,
    entity_id_from_result: Callable[[object], str | None] | None = None,
    before_payload=None,
    after_payload=None,
    action: Callable[[], object],
    request: Request | None = None,
):
    try:
        result = action()
        if entity_id is None and entity_id_from_result is not None:
            try:
                entity_id = entity_id_from_result(result)
            except Exception:
                entity_id = None
        write_audit_log(
            db,
            table_name=table_name,
            entity_id=entity_id,
            operation=operation,
            actor_user_id=actor_user_id,
            before_payload=before_payload,
            after_payload=after_payload,
            success=True,
            request_id=request.headers.get("X-Request-ID") if request else None,
            endpoint=str(request.url.path) if request else None,
            method=request.method if request else None,
            ip_address=request.client.host if request and request.client else None,
            user_agent=request.headers.get("User-Agent") if request else None,
        )
        return result
    except HTTPException as exc:
        db.rollback()
        write_audit_log(
            db,
            table_name=table_name,
            entity_id=entity_id,
            operation=operation,
            actor_user_id=actor_user_id,
            before_payload=before_payload,
            after_payload=after_payload,
            success=False,
            error_message=str(exc.detail),
            request_id=request.headers.get("X-Request-ID") if request else None,
            endpoint=str(request.url.path) if request else None,
            method=request.method if request else None,
            ip_address=request.client.host if request and request.client else None,
            user_agent=request.headers.get("User-Agent") if request else None,
        )
        raise
    except Exception as exc:
        db.rollback()
        write_audit_log(
            db,
            table_name=table_name,
            entity_id=entity_id,
            operation=operation,
            actor_user_id=actor_user_id,
            before_payload=before_payload,
            after_payload=after_payload,
            success=False,
            error_message=str(exc),
            request_id=request.headers.get("X-Request-ID") if request else None,
            endpoint=str(request.url.path) if request else None,
            method=request.method if request else None,
            ip_address=request.client.host if request and request.client else None,
            user_agent=request.headers.get("User-Agent") if request else None,
        )
        raise HTTPException(status_code=500, detail="Internal server error") from exc
