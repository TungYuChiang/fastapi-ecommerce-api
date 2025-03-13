#!/usr/bin/env python
"""
RabbitMQ 消息消費者啟動腳本
"""
import logging
import argparse
import time
import sys
import os

# 將項目根目錄添加到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.messaging.order_events import OrderEventConsumer

# 配置日誌
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def start_order_created_consumer():
    """啟動訂單創建事件消費者"""
    logger.info("正在啟動訂單創建事件消費者...")
    consumer = OrderEventConsumer()
    try:
        consumer.start_order_created_consumer()
    except KeyboardInterrupt:
        logger.info("收到中斷信號，正在關閉消費者...")
    finally:
        consumer.close()
        logger.info("訂單創建事件消費者已關閉")


def start_payment_processed_consumer():
    """啟動支付處理事件消費者"""
    logger.info("正在啟動支付處理事件消費者...")
    consumer = OrderEventConsumer()
    try:
        consumer.start_payment_processed_consumer()
    except KeyboardInterrupt:
        logger.info("收到中斷信號，正在關閉消費者...")
    finally:
        consumer.close()
        logger.info("支付處理事件消費者已關閉")


def declare_queues():
    """聲明所需的隊列"""
    logger.info("正在聲明所需的隊列...")
    consumer = OrderEventConsumer()
    try:
        consumer.declare_queues()
        logger.info("隊列聲明成功")
    finally:
        consumer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="訂單消息隊列消費者")
    parser.add_argument(
        "--queue",
        type=str,
        choices=["order_created", "payment_processed", "all", "setup"],
        default="all",
        help="要消費的隊列名稱，或使用 'setup' 僅創建隊列",
    )

    args = parser.parse_args()

    if args.queue == "setup":
        declare_queues()
    elif args.queue == "order_created":
        # 先聲明隊列再啟動消費者
        declare_queues()
        start_order_created_consumer()
    elif args.queue == "payment_processed":
        start_payment_processed_consumer()
    elif args.queue == "all":
        logger.info("正在啟動所有消費者...")
        import threading

        # 創建線程以並行運行多個消費者
        order_thread = threading.Thread(target=start_order_created_consumer)
        payment_thread = threading.Thread(target=start_payment_processed_consumer)

        # 啟動線程
        order_thread.start()
        payment_thread.start()

        try:
            # 等待線程完成
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("收到中斷信號，請等待所有消費者關閉...")

        logger.info("所有消費者已關閉")

# 要啟動此消費者，運行:
# python scripts/consumer.py --queue all