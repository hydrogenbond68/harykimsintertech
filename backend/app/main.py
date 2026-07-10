from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, products, orders, payments, reviews, wishlist, category_brand, users
from .database.session import engine, Base
from .config.config import settings

# Create database tables (in production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Harykims Intertech API", version="1.0.0")

# Set up CORS
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(wishlist.router, prefix="/api")
app.include_router(category_brand.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Harykims Intertech API"}
