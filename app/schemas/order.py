from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus, PaymentMethod


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    payment_method: Optional[PaymentMethod] = None


class OrderResponse(OrderBase):
    id: int
    order_number: str
    total_amount: float
    status: OrderStatus
    payment_method: Optional[PaymentMethod] = None
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True


class OrderListResponse(BaseModel):
    id: int
    order_number: str
    total_amount: float
    status: OrderStatus
    created_at: datetime

    class Config:
        orm_mode = True
