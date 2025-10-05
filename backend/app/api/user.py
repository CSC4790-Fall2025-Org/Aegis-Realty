from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud.user import (
    get_user_by_firebase_uid,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)
from app.models.user import User
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_account(
        user_data: UserCreate,
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):

    existing_user = get_user_by_firebase_uid(db, current_user['uid'])
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered"
        )

    if user_data.email != current_user.get('email'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must match authenticated user"
        )

    new_user = create_user(
        db=db,
        user_data=user_data,
        firebase_uid=current_user['uid'],
        display_name=current_user.get('name')
    )

    return new_user


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    user = get_user_by_firebase_uid(db, current_user['uid'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    return user


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
        user_update: UserUpdate,
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    user = get_user_by_firebase_uid(db, current_user['uid'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    # Only allow updating display_name for regular users
    update_data = {"display_name": user_update.display_name}
    updated_user = update_user(db, user.id, **update_data)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    """Delete current user account"""
    user = get_user_by_firebase_uid(db, current_user['uid'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    success = delete_user(db, user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id_endpoint(
        user_id: int,
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    """Get user by ID"""
    # Check if requesting own profile
    requesting_user = get_user_by_firebase_uid(db, current_user['uid'])
    if not requesting_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    if requesting_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only access own profile"
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_by_id(
        user_id: int,
        user_update: UserUpdate,
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    """Update user by ID"""
    # Check if updating own profile
    requesting_user = get_user_by_firebase_uid(db, current_user['uid'])
    if not requesting_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    if requesting_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update own profile"
        )

    # Only allow updating display_name for regular users
    update_data = {"display_name": user_update.display_name}
    updated_user = update_user(db, user_id, **update_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
        user_id: int,
        current_user=Depends(get_current_user(required=True)),
        db: Session = Depends(get_db)
):
    """Delete user by ID"""
    # Check if deleting own profile
    requesting_user = get_user_by_firebase_uid(db, current_user['uid'])
    if not requesting_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered"
        )

    if requesting_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete own profile"
        )

    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.get("/", response_model=List[UserResponse])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        approved_only: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get list of users (basic endpoint - could add admin restrictions later)"""
    query = db.query(User)

    if approved_only is not None:
        query = query.filter(User.is_approved == approved_only)

    users = query.offset(skip).limit(limit).all()
    return users