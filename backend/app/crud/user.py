from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Optional

def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[User]:
    return db.query(User).filter(User.firebase_uid == firebase_uid).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_data: UserCreate, firebase_uid: str, display_name: str = None) -> User:
    db_user = User(
        firebase_uid=firebase_uid,
        email=user_data.email,
        display_name=user_data.display_name or display_name,
        is_approved=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    """
    Update user fields by user_id. Pass fields to update as keyword arguments.
    Returns the updated user or None if not found.
    """
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    return None
    
def update_user_approval(db: Session, user_id: int, is_approved: bool) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        user.is_approved = is_approved
        db.commit()
        db.refresh(user)
    return user


