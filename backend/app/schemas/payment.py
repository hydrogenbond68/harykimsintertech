from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    amount: float
    currency: str = "KES"
    payment_method: Optional[str] = None

class PaymentCreate(PaymentBase):
    order_id: int

class PaymentUpdate(BaseModel):
    payment_status: str
    transaction_reference: Optional[str] = None
    dodo_payment_id: Optional[str] = None

class Payment(PaymentBase):
    id: int
    user_id: int
    order_id: int
    dodo_payment_id: Optional[str] = None
    payment_status: str
    transaction_reference: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    payment: Payment
    checkout_url: Optional[str] = None
