import os
from celery import Celery

# 從環境變數獲取 Redis URL，如果不存在則使用默認值
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# 創建Celery實例
celery_app = Celery(
    "ecommerce",
    broker=redis_url,
    backend=redis_url,
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
