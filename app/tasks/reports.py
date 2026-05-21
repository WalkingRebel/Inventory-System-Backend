import time
from app.core.celery_app import celery_app

@celery_app.task(name="reports.long_report", bind=True)
def long_report(self, seconds: int = 20):
    for i in range(seconds):
        self.update_state(state="PROGRESS", meta={"current": i + 1, "total": seconds})
        time.sleep(1)
    return {"done": True}