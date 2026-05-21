from app.core.celery_app import celery_app

@celery_app.task(name="debug.fail")
def fail():
    raise RuntimeError("ERRORRRRRRRRRRRR")

@celery_app.task(
    name="debug.retry",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3},
    bind=True,
    retry_backoff=True,
)

def retry(self):
    raise Exception("force retry")