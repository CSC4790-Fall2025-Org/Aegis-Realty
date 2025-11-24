from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.core import get_db
from app.models import User, Property
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.schemas.property import PropertyBase
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

@router.post("/{user_id}/favorites/{property_id}")
def add_favorite_property(
        user_id: int,
        property_id: int,
        db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    property_exists = db.query(Property).filter(Property.id == property_id).first()
    if not property_exists:
        raise HTTPException(status_code=404, detail="Property not found")

    if not user.favorite_properties:
        user.favorite_properties = []

    if property_id in user.favorite_properties:
        raise HTTPException(status_code=400, detail="Property already in favorites")

    user.favorite_properties = user.favorite_properties + [property_id]
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

@router.get("/{user_id}/favorites", response_model=List[PropertyBase])
def get_favorite_properties(
        user_id: int,
        db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.favorite_properties:
        return []

    properties = db.query(Property).filter(
        Property.id.in_(user.favorite_properties)
    ).all()
    return [PropertyBase.model_validate(p) for p in properties]

@router.delete("/{user_id}/favorites/{property_id}")
def remove_favorite_property(
        user_id: int,
        property_id: int,
        db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.favorite_properties or property_id not in user.favorite_properties:
        raise HTTPException(status_code=404, detail="Property not in favorites")

    user.favorite_properties = [id for id in user.favorite_properties if id != property_id]
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)