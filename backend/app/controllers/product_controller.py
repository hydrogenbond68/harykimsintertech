from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from ..models.product import Product as ProductModel
from ..schemas.product import ProductCreate, ProductUpdate
from ..services.cloudinary_service import cloudinary_service

class ProductController:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100, category: str = None, brand: str = None, search: str = None):
        query = db.query(ProductModel)
        if category:
            query = query.filter(ProductModel.category == category)
        if brand:
            query = query.filter(ProductModel.brand == brand)
        if search:
            query = query.filter(ProductModel.name.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, product_id: int):
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create(self, db: Session, product_in: ProductCreate):
        new_product = ProductModel(**product_in.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    def update(self, db: Session, product_id: int, product_in: ProductUpdate):
        product = self.get_by_id(db, product_id)
        update_data = product_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product_id: int):
        product = self.get_by_id(db, product_id)
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}

    def upload_image(self, file: UploadFile):
        url = cloudinary_service.upload_image(file.file)
        if not url:
            raise HTTPException(status_code=500, detail="Failed to upload image")
        return {"url": url}

product_controller = ProductController()
