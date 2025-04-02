from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.order import PaymentMethod
from app.services.payment_service import PaymentService
from app.tasks.order_tasks import verify_payment_status

router = APIRouter(prefix="/payments", tags=["payments"])


class PaymentRequest(BaseModel):
    order_id: int
    payment_method: PaymentMethod


class PaymentVerificationRequest(BaseModel):
    order_id: int


@router.post("/process", status_code=status.HTTP_200_OK)
def process_payment(
    payment_data: PaymentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    result = PaymentService.process_payment(
        db, payment_data.order_id, payment_data.payment_method
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    # If payment is successful, asynchronously verify payment status in the background
    if result["success"]:
        # Use Celery task to asynchronously verify payment status
        verify_payment_status.delay(payment_data.order_id)

    return result


@router.get("/status/{order_id}", status_code=status.HTTP_200_OK)
def check_payment_status(order_id: int, db: Session = Depends(get_db)):
    result = PaymentService.verify_payment_status(db, order_id)

    if not result["verified"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["message"]
        )

    return result
