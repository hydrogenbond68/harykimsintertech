from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.wishlist import Wishlist as WishlistModel
from ..schemas.wishlist import WishlistCreate

class WishlistController:
    def add(self, db: Session, wishlist_in: WishlistCreate, user_id: int):
        # Check if already in wishlist
        item = db.query(WishlistModel).filter(
            WishlistModel.user_id == user_id,
            WishlistModel.product_id == wishlist_in.product_id
        ).first()
        
        if item:
            raise HTTPException(status_code=400, detail="Product already in wishlist")

        new_item = WishlistModel(
            user_id=user_id,
            product_id=wishlist_in.product_id
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    def get_my_wishlist(self, db: Session, user_id: int):
        return db.query(WishlistModel).filter(WishlistModel.user_id == user_id).all()

    def remove(self, db: Session, product_id: int, user_id: int):
        item = db.query(WishlistModel).filter(
            WishlistModel.user_id == user_id,
            WishlistModel.product_id == product_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in wishlist")
        
        db.delete(item)
        db.commit()
        return {"message": "Item removed from wishlist"}

wishlist_controller = WishlistController()
