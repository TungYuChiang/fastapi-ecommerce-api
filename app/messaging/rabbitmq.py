import pika
import json
import logging
import os
from typing import Callable, Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """RabbitMQ client class for handling message sending and receiving"""

    def __init__(self, rabbitmq_url=None):
        # Get RabbitMQ URL from environment variable, use default if not present
        self.rabbitmq_url = rabbitmq_url or os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        
        # Parse URL
        url = urlparse(self.rabbitmq_url)
        self.host = url.hostname or "localhost"
        self.port = url.port or 5672
        self.username = url.username or "guest"
        self.password = url.password or "guest"
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ server"""
        if self.connection is None or self.connection.is_closed:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info(f"Connected to RabbitMQ server: {self.host}:{self.port}")
        return self.channel

    def close(self):
        """Close RabbitMQ connection"""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ connection closed")

    def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
        """Declare an exchange"""
        channel = self.connect()
        channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type, durable=True
        )
        logger.info(f"Exchange declared: {exchange_name}, type: {exchange_type}")

    def declare_queue(self, queue_name: str):
        """Declare a queue"""
        channel = self.connect()
        channel.queue_declare(queue=queue_name, durable=True)
        logger.info(f"Queue declared: {queue_name}")

    def bind_queue(self, queue_name: str, exchange_name: str, routing_key: str):
        """Bind a queue to an exchange"""
        channel = self.connect()
        channel.queue_bind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )
        logger.info(
            f"Queue {queue_name} bound to exchange {exchange_name}, routing key: {routing_key}"
        )

    def publish_message(self, exchange: str, routing_key: str, message: Dict[str, Any]):
        """Publish a message to an exchange"""
        channel = self.connect()

        # Convert message to JSON string
        message_body = json.dumps(message)

        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type="application/json",
            ),
        )
        logger.info(f"Message published to {exchange}/{routing_key}: {message}")

    def consume_messages(self, queue_name: str, callback: Callable):
        """Consume messages from a queue"""
        channel = self.connect()

        def wrapped_callback(ch, method, properties, body):
            try:
                # Convert JSON string back to Python object
                message = json.loads(body)
                logger.info(f"Message received: {message}")
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=wrapped_callback)
        logger.info(f"Started consuming messages from queue {queue_name}...")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            logger.info("Message consumption stopped")
            self.close()
