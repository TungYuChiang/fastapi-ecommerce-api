from datetime import datetime
from app.messaging.rabbitmq import RabbitMQClient
from app.tasks.order_tasks import verify_payment_status, send_order_confirmation_email
import logging

logger = logging.getLogger(__name__)

# Define exchange and queue names
ORDER_EXCHANGE = "order_events"
ORDER_CREATED_QUEUE = "order_created"
PAYMENT_PROCESSED_QUEUE = "payment_processed"
ORDER_SHIPPED_QUEUE = "order_shipped"

# Define routing keys
ORDER_CREATED_KEY = "order.created"
PAYMENT_PROCESSED_KEY = "order.payment"
ORDER_SHIPPED_KEY = "order.shipped"


class OrderEventProducer:
    """Order event producer for publishing order-related events"""

    def __init__(self):
        self.rabbitmq = RabbitMQClient()
        self._setup_exchanges()

    def _setup_exchanges(self):
        """Set up exchanges and queues"""
        try:
            self.rabbitmq.connect()

            # Declare exchange
            self.rabbitmq.declare_exchange(ORDER_EXCHANGE, "direct")

            # Declare queues
            self.rabbitmq.declare_queue(ORDER_CREATED_QUEUE)
            self.rabbitmq.declare_queue(PAYMENT_PROCESSED_QUEUE)
            self.rabbitmq.declare_queue(ORDER_SHIPPED_QUEUE)

            # Bind queues to exchange
            self.rabbitmq.bind_queue(
                ORDER_CREATED_QUEUE, ORDER_EXCHANGE, ORDER_CREATED_KEY
            )
            self.rabbitmq.bind_queue(
                PAYMENT_PROCESSED_QUEUE, ORDER_EXCHANGE, PAYMENT_PROCESSED_KEY
            )
            self.rabbitmq.bind_queue(
                ORDER_SHIPPED_QUEUE, ORDER_EXCHANGE, ORDER_SHIPPED_KEY
            )

        except Exception as e:
            logger.error(f"Error setting up RabbitMQ exchanges and queues: {str(e)}")

    def publish_order_created(self, order_id: int, user_id: int, total_amount: float):
        """Publish order creation event"""
        message = {
            "event_type": "order_created",
            "order_id": order_id,
            "user_id": user_id,
            "total_amount": total_amount,
            "timestamp": str(datetime.now()),
        }

        try:
            self.rabbitmq.publish_message(
                exchange=ORDER_EXCHANGE, routing_key=ORDER_CREATED_KEY, message=message
            )
            logger.info(f"Order creation event published: {order_id}")
        except Exception as e:
            logger.error(f"Error publishing order creation event: {str(e)}")

    def publish_payment_processed(
        self, order_id: int, payment_status: str, payment_method: str
    ):
        """Publish payment processing event"""
        message = {
            "event_type": "payment_processed",
            "order_id": order_id,
            "payment_status": payment_status,
            "payment_method": payment_method,
            "timestamp": str(datetime.now()),
        }

        try:
            self.rabbitmq.publish_message(
                exchange=ORDER_EXCHANGE,
                routing_key=PAYMENT_PROCESSED_KEY,
                message=message,
            )
            logger.info(f"Payment processing event published: {order_id}, status: {payment_status}")
        except Exception as e:
            logger.error(f"Error publishing payment processing event: {str(e)}")

    def close(self):
        """Close connection"""
        self.rabbitmq.close()


class OrderEventConsumer:
    """Order event consumer for handling order-related events"""

    def __init__(self):
        self.rabbitmq = RabbitMQClient()

    def declare_queues(self):
        """Declare required queues and exchanges"""
        try:
            self.rabbitmq.connect()

            # Declare exchange
            self.rabbitmq.declare_exchange(ORDER_EXCHANGE, "topic")

            # Declare queues
            self.rabbitmq.declare_queue(ORDER_CREATED_QUEUE)
            self.rabbitmq.declare_queue(PAYMENT_PROCESSED_QUEUE)
            self.rabbitmq.declare_queue(ORDER_SHIPPED_QUEUE)

            # Bind queues to exchange
            self.rabbitmq.bind_queue(
                ORDER_CREATED_QUEUE, ORDER_EXCHANGE, ORDER_CREATED_KEY
            )
            self.rabbitmq.bind_queue(
                PAYMENT_PROCESSED_QUEUE, ORDER_EXCHANGE, PAYMENT_PROCESSED_KEY
            )
            self.rabbitmq.bind_queue(
                ORDER_SHIPPED_QUEUE, ORDER_EXCHANGE, ORDER_SHIPPED_KEY
            )

            logger.info("Successfully declared all queues and exchanges")
        except Exception as e:
            logger.error(f"Error declaring queues and exchanges: {str(e)}")
            raise

    def start_order_created_consumer(self):
        """Start consuming order creation events"""
        try:
            # Ensure queues are created
            self.declare_queues()

            def handle_order_created(message):
                order_id = message.get("order_id")
                logger.info(f"Processing order creation event: {order_id}")

                # Trigger async task to send order confirmation email
                send_order_confirmation_email.delay(order_id)

            self.rabbitmq.consume_messages(ORDER_CREATED_QUEUE, handle_order_created)
        except Exception as e:
            logger.error(f"Error consuming order creation event: {str(e)}")

    def start_payment_processed_consumer(self):
        """Start consuming payment processing events"""
        try:
            # Ensure queues are created
            self.declare_queues()

            def handle_payment_processed(message):
                order_id = message.get("order_id")
                payment_status = message.get("payment_status")
                logger.info(f"Processing payment event: {order_id}, status: {payment_status}")

                # Trigger async task to verify payment status
                if payment_status == "completed":
                    verify_payment_status.delay(order_id)

            self.rabbitmq.consume_messages(
                PAYMENT_PROCESSED_QUEUE, handle_payment_processed
            )
        except Exception as e:
            logger.error(f"Error consuming payment processing event: {str(e)}")

    def close(self):
        """Close connection"""
        self.rabbitmq.close()
