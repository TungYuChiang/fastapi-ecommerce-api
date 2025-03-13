from celery import Celery
from app.config.settings import REDIS_URL

# 創建Celery實例
celery_app = Celery(
    "ecommerce",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.order_tasks"],
)

# 可選配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # 只接受JSON序列化的任務
    result_serializer="json",
    timezone="Asia/Taipei",  # 設定時區
    enable_utc=True,
)
