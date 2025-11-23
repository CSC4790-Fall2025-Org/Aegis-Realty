from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None

class UserCreate(UserBase):
    firebase_id: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    favorite_properties: Optional[List[int]] = None
    is_approved: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    firebase_id: str
    favorite_properties: List[int] = []
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int