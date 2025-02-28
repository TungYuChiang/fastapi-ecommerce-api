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
        模擬支付處理過程
        """
        # 獲取訂單
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"success": False, "message": "訂單不存在"}

        if order.status != OrderStatus.PENDING:
            return {
                "success": False,
                "message": f"訂單狀態為 {order.status}，無法處理支付",
            }

        # 模擬支付處理
        # 在實際應用中，這裡會調用第三方支付API
        success = random.random() > 0.2  # 80% 成功率

        # 更新訂單狀態
        if success:
            order.status = OrderStatus.PAID
            order.payment_status = "completed"
            db.commit()
            db.refresh(order)

            # 發布支付處理事件到 RabbitMQ
            try:
                producer = OrderEventProducer()
                producer.publish_payment_processed(
                    order_id=order.id,
                    payment_status="completed",
                    payment_method=payment_method,
                )
                producer.close()
            except Exception as e:
                logger.error(f"發布支付處理事件時發生錯誤: {str(e)}")

            return {
                "success": True,
                "message": "支付成功",
                "transaction_id": f"TX-{random.randint(10000000, 99999999)}",
                "amount": order.total_amount,
                "payment_method": payment_method,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            order.payment_status = "failed"
            db.commit()
            db.refresh(order)

            # 發布支付處理事件到 RabbitMQ
            try:
                producer = OrderEventProducer()
                producer.publish_payment_processed(
                    order_id=order.id,
                    payment_status="failed",
                    payment_method=payment_method,
                )
                producer.close()
            except Exception as e:
                logger.error(f"發布支付處理事件時發生錯誤: {str(e)}")

            return {
                "success": False,
                "message": "支付失敗，請稍後重試",
                "error_code": f"ERR-{random.randint(1000, 9999)}",
            }

    @staticmethod
    def verify_payment_status(db: Session, order_id: int) -> dict:
        """
        模擬驗證支付狀態
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"verified": False, "message": "訂單不存在"}

        if order.payment_status == "completed":
            return {"verified": True, "status": "completed", "message": "支付已完成"}
        elif order.payment_status == "pending":
            return {"verified": True, "status": "pending", "message": "支付處理中"}
        else:
            return {"verified": True, "status": "failed", "message": "支付失敗"}
