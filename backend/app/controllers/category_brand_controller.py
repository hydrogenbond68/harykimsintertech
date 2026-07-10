from sqlalchemy.orm import Session
from ..models.product import Category as CategoryModel, Brand as BrandModel
from ..schemas.category_brand import CategoryCreate, BrandCreate

class CategoryBrandController:
    def get_categories(self, db: Session):
        return db.query(CategoryModel).all()

    def create_category(self, db: Session, category_in: CategoryCreate):
        new_category = CategoryModel(**category_in.dict())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    def get_brands(self, db: Session):
        return db.query(BrandModel).all()

    def create_brand(self, db: Session, brand_in: BrandCreate):
        new_brand = BrandModel(**brand_in.dict())
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand

category_brand_controller = CategoryBrandController()
