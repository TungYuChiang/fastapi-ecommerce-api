#!/usr/bin/env python
from app.celery_app import celery_app

if __name__ == "__main__":
    # 使用Python API啟動Celery worker
    # 這相當於在命令行運行: celery -A app.celery_app worker --loglevel=info
    argv = [
        "worker",
        "--loglevel=INFO",
        "-n",
        "ecommerce_worker@%h",  # worker名稱
        "--concurrency=4",  # 工作進程數量
        "--max-tasks-per-child=1000",  # 工作進程最大處理任務數
    ]

    celery_app.worker_main(argv)

# 要啟動此worker，只需運行:
# python worker.py
