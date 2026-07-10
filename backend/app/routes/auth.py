from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..schemas.user import UserCreate, User, Token, TokenRefresh, UserUpdate
from ..models.user import User as UserModel
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.deps import get_current_user
from ..controllers.auth_controller import auth_controller
from ..controllers.user_controller import user_controller

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.register(db, user_in)

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_controller.login(db, form_data.username, form_data.password)

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_in: TokenRefresh, db: Session = Depends(get_db)):
    return auth_controller.refresh_token(db, refresh_in.refresh_token)

@router.get("/profile", response_model=User)
def get_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=User)
def update_profile(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return user_controller.update_me(db, current_user, user_in)
