from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.session import get_db
from ..schemas.wishlist import WishlistItem, WishlistCreate
from ..auth.deps import get_current_user
from ..models.user import User
from ..controllers.wishlist_controller import wishlist_controller

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("/", response_model=WishlistItem)
def add_to_wishlist(
    wishlist_in: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return wishlist_controller.add(db, wishlist_in, current_user.id)

@router.get("/", response_model=List[WishlistItem])
def get_my_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return wishlist_controller.get_my_wishlist(db, current_user.id)

@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return wishlist_controller.remove(db, product_id, current_user.id)
