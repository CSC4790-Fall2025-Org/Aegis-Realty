from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.core import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.crud import (
    create_user,
    get_user_by_id,
    get_user_by_firebase_id,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_route(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            user_data=data,
            firebase_id=data.firebase_id,
            display_name=data.display_name
        )
        return user
    except IntegrityError:
        db.rollback()
        existing = get_user_by_firebase_id(db, data.firebase_id)
        if existing:
            return existing
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )


@router.get("/", response_model=List[UserResponse])
def get_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no users"
        )

    return users


@router.get("/firebase/{firebase_id}", response_model=UserResponse)
def get_user_by_firebase_id_route(firebase_id: str, db: Session = Depends(get_db)):
    user = get_user_by_firebase_id(db, firebase_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/{id}", response_model=UserResponse)
def get_user_route(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch("/{id}", response_model=UserResponse)
def update_user_route(id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, id, **user_data.dict(exclude_unset=True))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)

    if not user:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    success = delete_user(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
