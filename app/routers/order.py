from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderResponse, OrderListResponse
from app.services.order_service import OrderService
from app.errors import NotFoundError


# 假設我們有一個簡單的用戶驗證機制
def get_current_user_id():
    # 在實際應用中，這應該從JWT令牌或會話中獲取用戶ID
    return 1  # 假設用戶ID為1


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    try:
        order = OrderService.create_order(db, order_data, current_user_id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    order = OrderService.get_order_by_id(db, order_id, current_user_id)
    if not order:
        raise NotFoundError(message="Order not found")
    return order


@router.get("/", response_model=List[OrderListResponse])
def get_user_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    orders = OrderService.get_user_orders(db, current_user_id, skip, limit)
    return orders
