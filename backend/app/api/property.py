from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.property_schemas import PropertyRecord
from app.models.property import Property
from app.core.database import get_db
from typing import List

router = APIRouter()

@router.get("/properties", response_model=List[PropertyRecord])
def read_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    return [PropertyRecord(
        id=str(p.id),
        formattedAddress=p.address,
        addressLine1=p.address,
        city=p.city,
        state=p.state,
        zipCode=p.zip_code,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        squareFootage=p.square_feet,
        yearBuilt=p.year_built,
        lastSalePrice=p.price
    ) for p in properties]

@router.get("/properties/{property_id}", response_model=PropertyRecord)
def read_property(property_id: int, db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == property_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyRecord(
        id=str(p.id),
        formattedAddress=p.address,
        addressLine1=p.address,
        city=p.city,
        state=p.state,
        zipCode=p.zip_code,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        squareFootage=p.square_feet,
        yearBuilt=p.year_built,
        lastSalePrice=p.price
    )
