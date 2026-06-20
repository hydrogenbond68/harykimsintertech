from sqlalchemy.orm import Session
from ..models.user import User as UserModel
from ..schemas.user import UserUpdate

class UserController:
    def update_me(self, db: Session, current_user: UserModel, user_in: UserUpdate):
        update_data = user_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        return current_user

user_controller = UserController()
