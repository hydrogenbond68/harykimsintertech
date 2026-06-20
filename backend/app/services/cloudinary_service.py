import cloudinary
import cloudinary.uploader
from ..config.config import settings

class CloudinaryService:
    def __init__(self):
        if settings.CLOUDINARY_URL:
            cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL)

    def upload_image(self, file, folder="products"):
        try:
            result = cloudinary.uploader.upload(file, folder=folder)
            return result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            return None

    def delete_image(self, public_id):
        try:
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception as e:
            print(f"Cloudinary deletion failed: {e}")
            return False

cloudinary_service = CloudinaryService()
