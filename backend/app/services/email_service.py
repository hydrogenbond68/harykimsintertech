import resend
from ..config.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self):
        self.resend_api_key = None

        # SMTP configuration from settings
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD

    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None):
        if not self.smtp_user or not self.smtp_password:
            print(f"Email would be sent to {to_email} with subject: {subject}")
            return

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.smtp_user
        message["To"] = to_email

        message.attach(MIMEText(body, "plain"))

        if html_body:
            message.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(
                    self.smtp_user,
                    to_email,
                    message.as_string()
                )
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_order_received(self, to_email: str, order_number: str, total_amount: float):
        subject = f"Order Received - {order_number}"
        body = (
            f"We have received your order {order_number}. "
            f"Please proceed to payment to complete your purchase. "
            f"Total amount: {total_amount}"
        )
        html_body = f"""
        <h1>Order Received</h1>
        <p>We have received your order <strong>{order_number}</strong>.</p>
        <p>Please proceed to payment to complete your purchase.</p>
        <p>Total amount: <strong>{total_amount}</strong></p>
        """
        self.send_email(to_email, subject, body, html_body)

    def send_payment_confirmation(self, to_email: str, order_number: str, amount: float):
        subject = f"Payment Confirmed - {order_number}"
        body = (
            f"Thank you! Your payment for order {order_number} has been confirmed. "
            f"We are now processing your order. Amount paid: {amount}"
        )
        html_body = f"""
        <h1>Payment Confirmed!</h1>
        <p>Thank you! Your payment for order <strong>{order_number}</strong> has been confirmed.</p>
        <p>We are now processing your order.</p>
        <p>Amount paid: <strong>{amount}</strong></p>
        """
        self.send_email(to_email, subject, body, html_body)


email_service = EmailService()
