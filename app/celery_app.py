from celery import Celery

# 創建Celery實例
celery_app = Celery(
    "ecommerce",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
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
