from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "inventroy-system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.reports"],
)

celery_app.conf.task_routes = {
    "reports.*": {"queue": "reports"},
    "purchase.*": {"queue": "purchase"},
    "sales.*": {"queue": "sales"},
    "inventory.*": {"queue": "inventory"},
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=True,

    worker_send_task_events=True,
    task_track_started=True,
    task_send_sent_event=True,
)

include=[
  "app.tasks.reports",
  "app.tasks.purchase",
  "app.tasks.sales",
  "app.tasks.inventory",
  "app.tasks.debug",
]
