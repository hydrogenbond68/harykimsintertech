from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import StreamingResponse

from ..database.session import get_db
from ..schemas.order import Order, OrderCreate, OrderUpdate
from ..auth.deps import get_current_user, get_admin_user
from ..models.user import User
from ..services.pdf_service import pdf_service
from ..controllers.order_controller import order_controller

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_controller.create(db, order_in, current_user.id, current_user.email)

@router.get("/my-orders", response_model=List[Order])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_controller.get_my_orders(db, current_user.id)

@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_controller.get_by_id(db, order_id, current_user.id, current_user.role)

@router.get("/", response_model=List[Order])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return order_controller.get_all(db, skip, limit)

@router.put("/{order_id}", response_model=Order)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return order_controller.update_status(db, order_id, order_update)

@router.get("/{order_id}/invoice")
def download_invoice(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = order_controller.get_by_id(db, order_id, current_user.id, current_user.role)
    pdf_buffer = pdf_service.generate_invoice(order)
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice_{order.order_number}.pdf"}
    )
