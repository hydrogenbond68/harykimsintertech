from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.order import Order as OrderModel, OrderItem as OrderItemModel
from ..models.product import Product as ProductModel
from ..schemas.order import OrderCreate, OrderUpdate
from ..services.email_service import email_service
import random
import string

class OrderController:
    def _generate_order_number(self):
        return "HK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def create(self, db: Session, order_in: OrderCreate, user_id: int, user_email: str):
        # 1. Verify products and stock
        for item in order_in.items:
            product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Not enough stock for product {product.name}"
                )

        # 2. Create Order
        order_number = self._generate_order_number()
        new_order = OrderModel(
            user_id=user_id,
            order_number=order_number,
            subtotal=order_in.subtotal,
            tax=order_in.tax,
            shipping_fee=order_in.shipping_fee,
            total_amount=order_in.total_amount,
            currency=order_in.currency,
            shipping_address=order_in.shipping_address,
            payment_status="pending",
            order_status="pending"
        )
        db.add(new_order)
        db.flush()

        # 3. Create Order Items and update stock
        for item in order_in.items:
            order_item = OrderItemModel(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            db.add(order_item)
            
            # Deduct stock
            product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
            product.stock_quantity -= item.quantity

        db.commit()
        db.refresh(new_order)

        # Send "Order Received" email
        email_service.send_order_received(
            user_email,
            new_order.order_number,
            new_order.total_amount
        )

        return new_order

    def get_my_orders(self, db: Session, user_id: int):
        return db.query(OrderModel).filter(OrderModel.user_id == user_id).order_by(OrderModel.created_at.desc()).all()

    def get_by_id(self, db: Session, order_id: int, user_id: int, user_role: str):
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if user_role != "admin" and order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this order")
        
        return order

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(OrderModel).offset(skip).limit(limit).all()

    def update_status(self, db: Session, order_id: int, order_update: OrderUpdate):
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)
        
        db.commit()
        db.refresh(order)
        return order

order_controller = OrderController()
