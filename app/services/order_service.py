from sqlalchemy.orm import Session
import uuid
from typing import List
import logging

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate
from app.messaging.order_events import OrderEventProducer

logger = logging.getLogger(__name__)


class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:

        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        db_order = Order(
            order_number=order_number,
            user_id=user_id,
            total_amount=0,  
            status=OrderStatus.PENDING,
            payment_method=order_data.payment_method,
        )

        db.add(db_order)
        db.flush()  # 獲取訂單ID

        # 處理訂單項目
        total_amount = 0

        for item in order_data.items:
            # 獲取產品
            product = (
                db.query(Product).filter(Product.id == item.product_id).first()
            )
            if not product:
                db.rollback()
                raise ValueError(f"產品 ID {item.product_id} 不存在")

            # 創建訂單項目
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )

            db.add(order_item)

            # 計算總額
            total_amount += product.price * item.quantity

        db_order.total_amount = total_amount

        db.commit()
        db.refresh(db_order)

        # 發布訂單創建事件到 RabbitMQ
        try:
            producer = OrderEventProducer()
            producer.publish_order_created(
                order_id=db_order.id, user_id=user_id, total_amount=total_amount
            )
            producer.close()
        except Exception as e:
            logger.error(f"發布訂單創建事件時發生錯誤: {str(e)}")

        return db_order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user_id: int) -> Order:
        return (
            db.query(Order)
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_user_orders(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: OrderStatus) -> Order:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if db_order:
            db_order.status = status
            db.commit()
            db.refresh(db_order)
        return db_order
