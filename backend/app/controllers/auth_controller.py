from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User as UserModel, UserRole
from ..schemas.user import UserCreate, TokenRefresh
from ..auth.utils import get_password_hash, verify_password
from ..auth.jwt import create_access_token, create_refresh_token, decode_refresh_token

class AuthController:
    def register(self, db: Session, user_in: UserCreate):
        user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        
        # Check if this is the first user, if so make them admin
        user_count = db.query(UserModel).count()
        role = UserRole.ADMIN if user_count == 0 else UserRole.USER

        new_user = UserModel(
            email=user_in.email,
            full_name=user_in.full_name,
            phone_number=user_in.phone_number,
            password_hash=get_password_hash(user_in.password),
            role=role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login(self, db: Session, username, password):
        user = db.query(UserModel).filter(UserModel.email == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_token(self, db: Session, refresh_token: str):
        payload = decode_refresh_token(refresh_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        
        email = payload.get("sub")
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        new_access_token = create_access_token(data={"sub": user.email, "role": user.role})
        new_refresh_token = create_refresh_token(data={"sub": user.email})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

auth_controller = AuthController()
