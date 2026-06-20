from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.session import get_db
from ..schemas.category_brand import Category, CategoryCreate, Brand, BrandCreate
from ..auth.deps import get_admin_user
from ..controllers.category_brand_controller import category_brand_controller

router = APIRouter(tags=["categories & brands"])

@router.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    return category_brand_controller.get_categories(db)

@router.post("/categories", response_model=Category)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return category_brand_controller.create_category(db, category_in)

@router.get("/brands", response_model=List[Brand])
def get_brands(db: Session = Depends(get_db)):
    return category_brand_controller.get_brands(db)

@router.post("/brands", response_model=Brand)
def create_brand(brand_in: BrandCreate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return category_brand_controller.create_brand(db, brand_in)
