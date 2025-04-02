from app.celery_app import celery_app
from celery.utils.log import get_task_logger
import time
from app.database import SessionLocal
from app.models.order import Order, OrderStatus

logger = get_task_logger(__name__)


@celery_app.task(name="verify_payment_status")
def verify_payment_status(order_id: int):
    """
    Asynchronous task for verifying payment status
    """
    logger.info(f"Starting verification of payment status for order #{order_id}")

    # Simulate network delay
    time.sleep(5)

    # In a real system, this would call a payment provider's API

    # Get database connection
    db = SessionLocal()
    try:
        # Get order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.error(f"Order #{order_id} does not exist")
            return {"success": False, "message": "Order does not exist"}

        # If order status is already paid, return success
        if order.status == OrderStatus.PAID:
            logger.info(f"Payment for order #{order_id} confirmed")
            return {"success": True, "status": "paid", "message": "Payment confirmed"}

        # Simulate payment confirmation logic
        if order.payment_status == "completed":
            order.status = OrderStatus.PAID
            db.commit()
            logger.info(f"Payment for order #{order_id} confirmed and updated")
            return {"success": True, "status": "paid", "message": "Payment confirmed and updated"}

        logger.warning(f"Payment for order #{order_id} not yet completed")
        return {
            "success": False,
            "status": order.payment_status,
            "message": "Payment not yet completed",
        }

    finally:
        db.close()


@celery_app.task(name="send_order_confirmation_email")
def send_order_confirmation_email(
    order_id: int, user_email: str = "example@example.com"
):
    """
    Asynchronous order confirmation email sending
    """
    logger.info(f"Preparing to send order #{order_id} confirmation email to {user_email}")

    # Simulate email sending delay
    time.sleep(3)

    # In a real system, this would call an email service
    logger.info(f"Order #{order_id} confirmation email successfully sent to {user_email}")

    return {"success": True, "message": f"Order confirmation email sent to {user_email}"}
