from dodopayments import DodoPayments
from ..config.config import settings
import os

class DodoService:
    def __init__(self):
        self.client = None
        if settings.DODO_API_KEY:
            self.client = DodoPayments(
                bearer_token=settings.DODO_API_KEY,
                environment=settings.DODO_ENVIRONMENT
            )

    def create_checkout_session(self, amount, currency, customer_email, product_name, order_id):
        if not self.client:
            return None
        
        try:
            # Note: The actual parameters might vary based on the SDK version
            # Using basic structure based on documentation
            session = self.client.checkout_sessions.create(
                customer={
                    "email": customer_email,
                    "name": customer_email.split('@')[0]
                },
                product_cart=[
                    {
                        "name": product_name,
                        "price": int(amount * 100), 
                        "quantity": 1
                    }
                ],
                billing={
                    "country": "KE" # Default to Kenya as per project context
                },
                metadata={
                    "order_id": str(order_id)
                },
                return_url=f"{settings.FRONTEND_URL}/order-success/{order_id}"
            )
            return session
        except Exception as e:
            print(f"Dodo Payment Session creation failed: {e}")
            return None

    def verify_webhook(self, payload: str, headers: dict):
        if not self.client or not settings.DODO_WEBHOOK_SECRET:
            return None
        
        try:
            # The SDK uses unwrap to verify and parse webhooks
            event = self.client.webhooks.unwrap(
                payload=payload,
                headers={
                    "webhook-id": headers.get("webhook-id"),
                    "webhook-signature": headers.get("webhook-signature"),
                    "webhook-timestamp": headers.get("webhook-timestamp"),
                },
                secret=settings.DODO_WEBHOOK_SECRET
            )
            return event
        except Exception as e:
            print(f"Webhook verification failed: {e}")
            return None

dodo_service = DodoService()
