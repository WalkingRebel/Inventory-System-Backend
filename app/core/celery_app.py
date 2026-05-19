from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "inventroy-system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.reports"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_concept=["json"],
    result_serializer="json",
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=True,
)