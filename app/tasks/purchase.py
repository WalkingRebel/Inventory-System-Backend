import time
from app.core.celery_app import celery_app

@celery_app.task(name="purchase.long_job")
def long_job(seconds: int = 15):
    time.sleep(seconds)
    return {"purchase": "ok"}