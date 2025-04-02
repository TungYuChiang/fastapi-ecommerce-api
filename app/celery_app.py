from celery import Celery
from app.config.settings import REDIS_URL

# Create Celery instance
celery_app = Celery(
    "ecommerce",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.order_tasks"],
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Only accept JSON serialized tasks
    result_serializer="json",
    timezone="Asia/Taipei",  # Set timezone
    enable_utc=True,
)
