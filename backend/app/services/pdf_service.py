from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

class PDFService:
    def generate_invoice(self, order):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.drawString(100, 750, f"Invoice for Order: {order.order_number}")
        p.drawString(100, 730, f"Date: {order.created_at}")
        p.drawString(100, 710, f"Customer: {order.user.full_name}")
        
        y = 680
        p.drawString(100, y, "Items:")
        y -= 20
        for item in order.items:
            p.drawString(120, y, f"{item.product.name} - {item.quantity} x {item.price}")
            y -= 20
        
        p.drawString(100, y - 20, f"Total Amount: {order.currency} {order.total_amount}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer

pdf_service = PDFService()
