#!/usr/bin/env python
"""
電子商務平台統一命令行介面
"""
import argparse
import os
import sys
import subprocess


def run_api():
    """啟動 API 服務器"""
    print("正在啟動 API 服務器...")
    subprocess.run(["python", "api.py"])


def run_worker():
    """啟動 Celery Worker"""
    print("正在啟動 Celery Worker...")
    subprocess.run(["python", "scripts/worker.py"])


def run_consumer(queue="all"):
    """啟動 RabbitMQ 消費者"""
    print(f"正在啟動 RabbitMQ 消費者 (隊列: {queue})...")
    subprocess.run(["python", "scripts/consumer.py", "--queue", queue])


def create_tables():
    """創建數據庫表格"""
    print("正在創建數據庫表格...")
    subprocess.run(["python", "scripts/create_tables.py"])


def run_tests():
    """運行測試"""
    print("正在運行測試...")
    subprocess.run(["python", "tests/test_order_flow.py"])


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="電子商務平台命令行工具")
    parser.add_argument(
        "command",
        choices=["api", "worker", "consumer", "create-tables", "test", "all"],
        help="要執行的命令",
    )
    parser.add_argument(
        "--queue",
        choices=["order_created", "payment_processed", "all", "setup"],
        default="all",
        help="消費者隊列名稱 (僅適用於 consumer 命令)",
    )

    args = parser.parse_args()

    if args.command == "api":
        run_api()
    elif args.command == "worker":
        run_worker()
    elif args.command == "consumer":
        run_consumer(args.queue)
    elif args.command == "create-tables":
        create_tables()
    elif args.command == "test":
        run_tests()
    elif args.command == "all":
        # 使用多進程啟動所有服務
        import multiprocessing

        # 先創建表格
        create_tables()

        # 啟動所有服務
        processes = [
            multiprocessing.Process(target=run_api),
            multiprocessing.Process(target=run_worker),
            multiprocessing.Process(target=run_consumer),
        ]

        # 啟動所有進程
        for p in processes:
            p.start()

        try:
            # 等待所有進程完成
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print("收到中斷信號，正在關閉所有服務...")
            for p in processes:
                p.terminate()
            print("所有服務已關閉")


if __name__ == "__main__":
    main()

# 使用方法:
# python run.py api          # 啟動 API 服務器
# python run.py worker       # 啟動 Celery Worker
# python run.py consumer     # 啟動所有 RabbitMQ 消費者
# python run.py create-tables # 創建數據庫表格
# python run.py test         # 運行測試
# python run.py all          # 啟動所有服務