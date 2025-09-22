from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegistration
from typing import Optional

def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[User]:
    return db.query(User).filter(User.firebase_uid == firebase_uid).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_data: UserRegistration, firebase_uid: str, display_name: str = None) -> User:
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

def update_user_approval(db: Session, user_id: int, is_approved: bool) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        user.is_approved = is_approved
        db.commit()
        db.refresh(user)
    return user
