from sqlalchemy.orm import Session
import random
from datetime import datetime
import logging
from app.models.order import Order, OrderStatus
from app.messaging.order_events import OrderEventProducer

logger = logging.getLogger(__name__)


class PaymentService:
    @staticmethod
    def process_payment(db: Session, order_id: int, payment_method: str) -> dict:
        """
        Simulate payment processing
        """
        # Get order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"success": False, "message": "Order does not exist"}

        if order.status != OrderStatus.PENDING:
            return {
                "success": False,
                "message": f"Order status is {order.status}, cannot process payment",
            }

        # Simulate payment processing
        # In a real application, this would call a third-party payment API
        success = random.random() > 0.2  # 80% success rate

        # Update order status
        if success:
            order.status = OrderStatus.PAID
            order.payment_status = "completed"
            db.commit()
            db.refresh(order)

            # Publish payment processing event to RabbitMQ
            try:
                producer = OrderEventProducer()
                producer.publish_payment_processed(
                    order_id=order.id,
                    payment_status="completed",
                    payment_method=payment_method,
                )
                producer.close()
            except Exception as e:
                logger.error(f"Error publishing payment processing event: {str(e)}")

            return {
                "success": True,
                "message": "Payment successful",
                "transaction_id": f"TX-{random.randint(10000000, 99999999)}",
                "amount": order.total_amount,
                "payment_method": payment_method,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            order.payment_status = "failed"
            db.commit()
            db.refresh(order)

            # Publish payment processing event to RabbitMQ
            try:
                producer = OrderEventProducer()
                producer.publish_payment_processed(
                    order_id=order.id,
                    payment_status="failed",
                    payment_method=payment_method,
                )
                producer.close()
            except Exception as e:
                logger.error(f"Error publishing payment processing event: {str(e)}")

            return {
                "success": False,
                "message": "Payment failed, please try again later",
                "error_code": f"ERR-{random.randint(1000, 9999)}",
            }

    @staticmethod
    def verify_payment_status(db: Session, order_id: int) -> dict:
        """
        Simulate payment status verification
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"verified": False, "message": "Order does not exist"}

        if order.payment_status == "completed":
            return {"verified": True, "status": "completed", "message": "Payment completed"}
        elif order.payment_status == "pending":
            return {"verified": True, "status": "pending", "message": "Payment processing"}
        else:
            return {"verified": True, "status": "failed", "message": "Payment failed"}
