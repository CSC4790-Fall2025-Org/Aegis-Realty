from fastapi import Header, HTTPException, Depends
from firebase_admin import auth
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# Global auth setting - change to True for production
REQUIRE_AUTH = False

def get_current_user(required: bool = REQUIRE_AUTH):
    async def auth_dependency(authorization: str = Header(None)):
        if not authorization:
            if required:
                raise HTTPException(status_code=401, detail="Authentication required")
            return None

        if not authorization.startswith("Bearer "):
            if required:
                raise HTTPException(status_code=401, detail="Invalid authorization format")
            return None

        try:
            token = authorization.split("Bearer ")[1]
            return auth.verify_id_token(token)
        except Exception as e:
            if required:
                raise HTTPException(status_code=401, detail="Invalid token")
            return None

    return auth_dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
