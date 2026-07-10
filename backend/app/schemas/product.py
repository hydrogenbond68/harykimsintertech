from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class BrandBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None

class Brand(BrandBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    slug: str
    description: str
    category: str
    brand: str
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int = 0
    sku: Optional[str] = None
    specifications: Optional[dict] = None
    featured: bool = False
    is_best_seller: bool = False
    is_trending: bool = False
    images: Optional[List[str]] = None
    status: str = "active"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    specifications: Optional[dict] = None
    featured: Optional[bool] = None
    is_best_seller: Optional[bool] = None
    is_trending: Optional[bool] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
