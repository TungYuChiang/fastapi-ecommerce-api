import pika
import json
import logging
from typing import Callable, Dict, Any

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """RabbitMQ 客戶端類，用於處理消息的發送和接收"""

    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """建立與 RabbitMQ 服務器的連接"""
        if self.connection is None or self.connection.is_closed:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info(f"已連接到 RabbitMQ 服務器: {self.host}:{self.port}")
        return self.channel

    def close(self):
        """關閉 RabbitMQ 連接"""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ 連接已關閉")

    def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
        """聲明一個交換機"""
        channel = self.connect()
        channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type, durable=True
        )
        logger.info(f"已聲明交換機: {exchange_name}, 類型: {exchange_type}")

    def declare_queue(self, queue_name: str):
        """聲明一個隊列"""
        channel = self.connect()
        channel.queue_declare(queue=queue_name, durable=True)
        logger.info(f"已聲明隊列: {queue_name}")

    def bind_queue(self, queue_name: str, exchange_name: str, routing_key: str):
        """將隊列綁定到交換機"""
        channel = self.connect()
        channel.queue_bind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )
        logger.info(
            f"已將隊列 {queue_name} 綁定到交換機 {exchange_name}, 路由鍵: {routing_key}"
        )

    def publish_message(self, exchange: str, routing_key: str, message: Dict[str, Any]):
        """發布消息到交換機"""
        channel = self.connect()

        # 將消息轉換為 JSON 字符串
        message_body = json.dumps(message)

        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # 使消息持久化
                content_type="application/json",
            ),
        )
        logger.info(f"消息已發布到 {exchange}/{routing_key}: {message}")

    def consume_messages(self, queue_name: str, callback: Callable):
        """從隊列消費消息"""
        channel = self.connect()

        def wrapped_callback(ch, method, properties, body):
            try:
                # 將 JSON 字符串轉換回 Python 對象
                message = json.loads(body)
                logger.info(f"收到消息: {message}")
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"處理消息時發生錯誤: {str(e)}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=wrapped_callback)
        logger.info(f"開始從隊列 {queue_name} 消費消息...")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            logger.info("消息消費已停止")
            self.close()
