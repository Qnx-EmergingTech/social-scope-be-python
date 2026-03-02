from celery_app import celery_app
import time
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=3)
def long_task(self, name: str):
    try:
        time.sleep(10)
        logger.info(f"Task completed for {name}")
        return f"Task completed for {name}"
    except Exception as e:
        raise self.retry(exc=e, countdown=5)