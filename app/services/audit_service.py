import json
from typing import Any
from sqlalchemy.orm import Session
from app.models.audit_logs import AuditLog


def _to_json(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, default=str, ensure_ascii=False)


def write_audit_log(
    db: Session,
    *,
    table_name: str,
    entity_id: str | None,
    operation: str,
    actor_user_id: int | None,
    before_payload: Any = None,
    after_payload: Any = None,
    success: bool = True,
    error_message: str | None = None,
    request_id: str | None = None,
    endpoint: str | None = None,
    method: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> None:
    log = AuditLog(
        table_name=table_name,
        entity_id=entity_id,
        operation=operation,
        actor_user_id=actor_user_id,
        before_payload=_to_json(before_payload),
        after_payload=_to_json(after_payload),
        success=success,
        error_message=error_message,
        request_id=request_id,
        endpoint=endpoint,
        method=method,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(log)
    db.commit()
