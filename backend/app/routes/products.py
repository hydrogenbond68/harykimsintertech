from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.session import get_db
from ..schemas.product import Product, ProductCreate, ProductUpdate
from ..auth.deps import get_admin_user
from ..controllers.product_controller import product_controller

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return product_controller.get_all(db, skip, limit, category, brand, search)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_controller.get_by_id(db, product_id)

@router.post("/", response_model=Product)
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_admin_user)
):
    return product_controller.create(db, product_in)

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, 
    product_in: ProductUpdate, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_admin_user)
):
    return product_controller.update(db, product_id, product_in)

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_admin_user)
):
    return product_controller.delete(db, product_id)

@router.post("/upload-image")
def upload_product_image(
    file: UploadFile = File(...),
    admin_user = Depends(get_admin_user)
):
    return product_controller.upload_image(file)
