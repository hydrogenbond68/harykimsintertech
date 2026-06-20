from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItem(OrderItemBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    subtotal: float
    tax: float = 0.0
    shipping_fee: float = 0.0
    total_amount: float
    currency: str = "KES"
    shipping_address: dict

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class OrderUpdate(BaseModel):
    payment_status: Optional[str] = None
    order_status: Optional[str] = None
    tracking_number: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    order_number: str
    payment_status: str
    order_status: str
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItem]

    class Config:
        from_attributes = True
