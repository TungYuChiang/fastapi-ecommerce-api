from app.celery_app import celery_app
from celery.utils.log import get_task_logger
import time
from app.database import SessionLocal
from app.models.order import Order, OrderStatus

logger = get_task_logger(__name__)


@celery_app.task(name="verify_payment_status")
def verify_payment_status(order_id: int):
    """
    異步驗證支付狀態的任務
    """
    logger.info(f"開始驗證訂單 #{order_id} 的支付狀態")

    # 模擬網絡延遲
    time.sleep(5)

    # 在實際系統中，這裡會調用支付提供商的API

    # 獲取數據庫連接
    db = SessionLocal()
    try:
        # 獲取訂單
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.error(f"訂單 #{order_id} 不存在")
            return {"success": False, "message": "訂單不存在"}

        # 如果訂單狀態已經是已支付，則返回成功
        if order.status == OrderStatus.PAID:
            logger.info(f"訂單 #{order_id} 支付已確認")
            return {"success": True, "status": "paid", "message": "支付已確認"}

        # 模擬支付確認邏輯
        if order.payment_status == "completed":
            order.status = OrderStatus.PAID
            db.commit()
            logger.info(f"訂單 #{order_id} 支付已確認並更新")
            return {"success": True, "status": "paid", "message": "支付已確認並更新"}

        logger.warning(f"訂單 #{order_id} 支付尚未完成")
        return {
            "success": False,
            "status": order.payment_status,
            "message": "支付尚未完成",
        }

    finally:
        db.close()


@celery_app.task(name="send_order_confirmation_email")
def send_order_confirmation_email(
    order_id: int, user_email: str = "example@example.com"
):
    """
    異步發送訂單確認郵件
    """
    logger.info(f"準備發送訂單 #{order_id} 確認郵件到 {user_email}")

    # 模擬郵件發送延遲
    time.sleep(3)

    # 在實際系統中，這裡會調用電子郵件服務
    logger.info(f"訂單 #{order_id} 確認郵件已成功發送到 {user_email}")

    return {"success": True, "message": f"訂單確認郵件已發送到 {user_email}"}
