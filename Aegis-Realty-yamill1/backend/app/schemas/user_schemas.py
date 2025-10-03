from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    display_name: Optional[str] = None
    password: Optional[str] = None  # Add if you want password on creation

class UserRead(BaseModel):
    id: int
    firebase_uid: str
    email: str
    display_name: Optional[str] = None
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    is_approved: Optional[bool] = None
    # Add other updatable fields as needed
