from sqlalchemy.orm import Session
from fastapi import HTTPException
import json
from ..models.payment_review import Payment as PaymentModel
from ..models.order import Order as OrderModel
from ..schemas.payment import PaymentCreate, PaymentUpdate
from ..services.dodo_service import dodo_service
from ..services.email_service import email_service

class PaymentController:
    def create_payment(self, db: Session, payment_in: PaymentCreate, user_id: int, user_email: str):
        # 1. Verify order exists and belongs to user
        order = db.query(OrderModel).filter(OrderModel.id == payment_in.order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to pay for this order")
        
        # 2. Initiate Dodo Payment
        product_name = f"Order #{order.order_number}"
        dodo_session = dodo_service.create_checkout_session(
            amount=payment_in.amount,
            currency=payment_in.currency,
            customer_email=user_email,
            product_name=product_name,
            order_id=order.id
        )

        dodo_payment_id = None
        extra_data = {}
        if dodo_session:
            # Assuming session_id is the correct field from the SDK
            try:
                dodo_payment_id = getattr(dodo_session, "session_id", None)
                if hasattr(dodo_session, "checkout_url"):
                    extra_data["checkout_url"] = dodo_session.checkout_url
            except Exception as e:
                print(f"Error extracting data from dodo_session: {e}")
        
        # 3. Create payment record
        new_payment = PaymentModel(
            user_id=user_id,
            order_id=payment_in.order_id,
            amount=payment_in.amount,
            currency=payment_in.currency,
            payment_method=payment_in.payment_method,
            payment_status="pending",
            dodo_payment_id=dodo_payment_id
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        
        return {
            "payment": new_payment,
            "checkout_url": extra_data.get("checkout_url")
        }

    def get_payment_by_order(self, db: Session, order_id: int, user_id: int, user_role: str):
        payment = db.query(PaymentModel).filter(PaymentModel.order_id == order_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        if payment.user_id != user_id and user_role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this payment")
        return payment

    def handle_webhook(self, db: Session, payload: str, headers: dict):
        # 1. Verify webhook signature
        event = dodo_service.verify_webhook(payload, headers)
        if not event:
            raise HTTPException(status_code=400, detail="Invalid webhook signature")
        
        # 2. Process event
        event_type = getattr(event, "type", None)
        data = getattr(event, "data", None)
        
        if event_type == "payment.succeeded":
            metadata = getattr(data, "metadata", {})
            order_id = metadata.get("order_id")
            
            if order_id:
                payment = db.query(PaymentModel).filter(PaymentModel.order_id == int(order_id)).first()
                if payment:
                    payment.payment_status = "paid"
                    order = db.query(OrderModel).filter(OrderModel.id == payment.order_id).first()
                    if order:
                        order.payment_status = "paid"
                        order.order_status = "processing"
                        
                        # Send payment confirmation email
                        email_service.send_payment_confirmation(
                            order.user.email,
                            order.order_number,
                            payment.amount
                        )
                    db.commit()
        
        return {"status": "success"}

payment_controller = PaymentController()
