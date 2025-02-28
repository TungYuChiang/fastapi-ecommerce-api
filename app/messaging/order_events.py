from app.messaging.rabbitmq import RabbitMQClient
from app.tasks.order_tasks import verify_payment_status, send_order_confirmation_email
import logging

logger = logging.getLogger(__name__)

# 定義交換機和隊列名稱
ORDER_EXCHANGE = "order_events"
ORDER_CREATED_QUEUE = "order_created"
PAYMENT_PROCESSED_QUEUE = "payment_processed"
ORDER_SHIPPED_QUEUE = "order_shipped"

# 定義路由鍵
ORDER_CREATED_KEY = "order.created"
PAYMENT_PROCESSED_KEY = "order.payment"
ORDER_SHIPPED_KEY = "order.shipped"


class OrderEventProducer:
    """訂單事件生產者，用於發布訂單相關事件"""

    def __init__(self):
        self.rabbitmq = RabbitMQClient()
        self._setup_exchanges()

    def _setup_exchanges(self):
        """設置交換機和隊列"""
        try:
            self.rabbitmq.connect()

            # 聲明交換機
            self.rabbitmq.declare_exchange(ORDER_EXCHANGE, "topic")

            # 聲明隊列
            self.rabbitmq.declare_queue(ORDER_CREATED_QUEUE)
            self.rabbitmq.declare_queue(PAYMENT_PROCESSED_QUEUE)
            self.rabbitmq.declare_queue(ORDER_SHIPPED_QUEUE)

            # 綁定隊列到交換機
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
            logger.error(f"設置 RabbitMQ 交換機和隊列時發生錯誤: {str(e)}")

    def publish_order_created(self, order_id: int, user_id: int, total_amount: float):
        """發布訂單創建事件"""
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
            logger.info(f"已發布訂單創建事件: {order_id}")
        except Exception as e:
            logger.error(f"發布訂單創建事件時發生錯誤: {str(e)}")

    def publish_payment_processed(
        self, order_id: int, payment_status: str, payment_method: str
    ):
        """發布支付處理事件"""
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
            logger.info(f"已發布支付處理事件: {order_id}, 狀態: {payment_status}")
        except Exception as e:
            logger.error(f"發布支付處理事件時發生錯誤: {str(e)}")

    def close(self):
        """關閉連接"""
        self.rabbitmq.close()


class OrderEventConsumer:
    """訂單事件消費者，用於處理訂單相關事件"""

    def __init__(self):
        self.rabbitmq = RabbitMQClient()

    def declare_queues(self):
        """聲明所需的隊列和交換機"""
        try:
            self.rabbitmq.connect()

            # 聲明交換機
            self.rabbitmq.declare_exchange(ORDER_EXCHANGE, "topic")

            # 聲明隊列
            self.rabbitmq.declare_queue(ORDER_CREATED_QUEUE)
            self.rabbitmq.declare_queue(PAYMENT_PROCESSED_QUEUE)
            self.rabbitmq.declare_queue(ORDER_SHIPPED_QUEUE)

            # 綁定隊列到交換機
            self.rabbitmq.bind_queue(
                ORDER_CREATED_QUEUE, ORDER_EXCHANGE, ORDER_CREATED_KEY
            )
            self.rabbitmq.bind_queue(
                PAYMENT_PROCESSED_QUEUE, ORDER_EXCHANGE, PAYMENT_PROCESSED_KEY
            )
            self.rabbitmq.bind_queue(
                ORDER_SHIPPED_QUEUE, ORDER_EXCHANGE, ORDER_SHIPPED_KEY
            )

            logger.info("成功聲明所有隊列和交換機")
        except Exception as e:
            logger.error(f"聲明隊列和交換機時發生錯誤: {str(e)}")
            raise

    def start_order_created_consumer(self):
        """開始消費訂單創建事件"""
        try:
            # 確保隊列已經被創建
            self.declare_queues()

            def handle_order_created(message):
                order_id = message.get("order_id")
                logger.info(f"處理訂單創建事件: {order_id}")

                # 觸發異步任務發送訂單確認郵件
                send_order_confirmation_email.delay(order_id)

            self.rabbitmq.consume_messages(ORDER_CREATED_QUEUE, handle_order_created)
        except Exception as e:
            logger.error(f"消費訂單創建事件時發生錯誤: {str(e)}")

    def start_payment_processed_consumer(self):
        """開始消費支付處理事件"""
        try:
            # 確保隊列已經被創建
            self.declare_queues()

            def handle_payment_processed(message):
                order_id = message.get("order_id")
                payment_status = message.get("payment_status")
                logger.info(f"處理支付處理事件: {order_id}, 狀態: {payment_status}")

                # 觸發異步任務驗證支付狀態
                if payment_status == "completed":
                    verify_payment_status.delay(order_id)

            self.rabbitmq.consume_messages(
                PAYMENT_PROCESSED_QUEUE, handle_payment_processed
            )
        except Exception as e:
            logger.error(f"消費支付處理事件時發生錯誤: {str(e)}")

    def close(self):
        """關閉連接"""
        self.rabbitmq.close()


# 確保導入消息處理所需的模塊
from datetime import datetime
