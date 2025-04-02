#!/usr/bin/env python
"""
Celery Worker Startup Script
"""
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.celery_app import celery_app

if __name__ == "__main__":
    # Use Python API to start Celery worker
    # This is equivalent to running in command line: celery -A app.celery_app worker --loglevel=info
    argv = [
        "worker",
        "--loglevel=INFO",
        "-n",
        "ecommerce_worker@%h",  # worker name
        "--concurrency=4",  # number of worker processes
        "--max-tasks-per-child=1000",  # maximum number of tasks per worker process
    ]

    celery_app.worker_main(argv)

# To start this worker, simply run:
# python scripts/worker.py