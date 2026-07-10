from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.session import get_db
from ..schemas.review import Review, ReviewCreate, ReviewUpdate
from ..auth.deps import get_current_user, get_admin_user
from ..models.user import User
from ..controllers.review_controller import review_controller

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return review_controller.create(db, review_in, current_user.id)

@router.get("/product/{product_id}", response_model=List[Review])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    return review_controller.get_by_product(db, product_id)

@router.get("/", response_model=List[Review])
def get_all_reviews(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return review_controller.get_all(db)

@router.put("/{review_id}", response_model=Review)
def update_review_status(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return review_controller.update_status(db, review_id, review_update)
