#!/usr/bin/env python
"""
Celery Worker 啟動腳本
"""
import sys
import os

# 將項目根目錄添加到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
# python scripts/worker.py