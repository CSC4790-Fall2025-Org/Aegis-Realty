from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None

class UserCreate(UserBase):
    firebase_id: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    is_approved: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    firebase_id: str
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int