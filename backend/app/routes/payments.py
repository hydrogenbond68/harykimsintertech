from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.session import get_db
from ..schemas.payment import Payment, PaymentCreate, PaymentUpdate, PaymentResponse
from ..auth.deps import get_current_user, get_admin_user
from ..models.user import User
from ..controllers.payment_controller import payment_controller

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return payment_controller.create_payment(db, payment_in, current_user.id, current_user.email)

@router.get("/order/{order_id}", response_model=Payment)
def get_payment_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return payment_controller.get_payment_by_order(db, order_id, current_user.id, current_user.role)

@router.post("/webhook")
async def dodo_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    headers = request.headers
    return payment_controller.handle_webhook(db, payload.decode(), headers)
