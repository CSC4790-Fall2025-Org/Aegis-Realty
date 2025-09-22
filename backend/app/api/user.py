from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.schemas.user import UserRegistration, UserResponse
from app.crud.user import get_user_by_firebase_uid, create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegistration,
    current_user=Depends(get_current_user(required=True)),
    db: Session = Depends(get_db)
):
    """Register a new user after Firebase authentication"""

    # Check if user already exists
    existing_user = get_user_by_firebase_uid(db, current_user['uid'])
    if existing_user:
        raise HTTPException(status_code=409, detail="User already registered")

    # Validate email matches Firebase token
    if user_data.email != current_user.get('email'):
        raise HTTPException(status_code=400, detail="Email must match authenticated user")

    # Create new user (unapproved by default)
    new_user = create_user(
        db=db,
        user_data=user_data,
        firebase_uid=current_user['uid'],
        display_name=current_user.get('name')
    )

    return new_user

@router.get("/current", response_model=UserResponse)
async def get_current_user_info(
    current_user=Depends(get_current_user(required=True)),
    db: Session = Depends(get_db)
):
    """Get current authenticated user information"""
    user = get_user_by_firebase_uid(db, current_user['uid'])
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    return user