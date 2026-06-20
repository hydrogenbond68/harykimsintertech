from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.payment_review import Review as ReviewModel
from ..schemas.review import ReviewCreate, ReviewUpdate

class ReviewController:
    def create(self, db: Session, review_in: ReviewCreate, user_id: int):
        # Check if user already reviewed this product
        existing_review = db.query(ReviewModel).filter(
            ReviewModel.user_id == user_id,
            ReviewModel.product_id == review_in.product_id
        ).first()
        
        if existing_review:
            raise HTTPException(status_code=400, detail="You have already reviewed this product")

        new_review = ReviewModel(
            user_id=user_id,
            **review_in.dict(),
            status="pending"
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    def get_by_product(self, db: Session, product_id: int):
        return db.query(ReviewModel).filter(
            ReviewModel.product_id == product_id,
            ReviewModel.status == "approved"
        ).all()

    def get_all(self, db: Session):
        return db.query(ReviewModel).all()

    def update_status(self, db: Session, review_id: int, review_update: ReviewUpdate):
        review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review.status = review_update.status
        db.commit()
        db.refresh(review)
        return review

review_controller = ReviewController()
