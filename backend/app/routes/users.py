from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..schemas.user import User, UserUpdate
from ..auth.deps import get_current_user
from ..models.user import User as UserModel
from ..controllers.user_controller import user_controller

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
def update_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return user_controller.update_me(db, current_user, user_in)
