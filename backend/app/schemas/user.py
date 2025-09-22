from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserRegistration(BaseModel):
    email: str
    display_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    firebase_uid: str
    email: str
    display_name: Optional[str] = None
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True