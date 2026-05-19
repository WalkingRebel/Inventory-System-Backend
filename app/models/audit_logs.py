from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    table_name = Column(String, nullable=False, index=True)
    entity_id = Column(String, nullable=True, index=True)
    operation = Column(String, nullable=False, index=True)  # CREATE / UPDATE / DELETE

    actor_user_id = Column(Integer, nullable=True, index=True)

    before_payload = Column(Text, nullable=True)  # JSON string
    after_payload = Column(Text, nullable=True)  # JSON string

    success = Column(Boolean, nullable=False, default=True)
    error_message = Column(Text, nullable=True)

    request_id = Column(String, nullable=True, index=True)
    endpoint = Column(String, nullable=True)
    method = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
