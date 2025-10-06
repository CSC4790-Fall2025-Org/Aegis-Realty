from sqlalchemy.orm import Session
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate
from typing import Optional, List

def get_all_properties(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None
) -> List[Property]:
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Property.state.ilike(f"%{state}%"))
    if property_type:
        query = query.filter(Property.property_type.ilike(f"%{property_type}%"))
    if min_price:
        query = query.filter(Property.last_sale_price >= min_price)
    if max_price:
        query = query.filter(Property.last_sale_price <= max_price)
    if bedrooms:
        query = query.filter(Property.bedrooms == bedrooms)
    return query.offset(skip).limit(limit).all()

def get_property_by_id(db: Session, property_id: int) -> Optional[Property]:
    return db.query(Property).filter(Property.id == property_id).first()

def create_property(db: Session, property_data: PropertyCreate) -> Property:
    db_property = Property(**property_data.dict(by_alias=False, exclude_unset=True))
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property_data: PropertyUpdate) -> Optional[Property]:
    property_obj = get_property_by_id(db, property_id)
    if property_obj:
        update_data = property_data.dict(by_alias=False, exclude_unset=True)
        for key, value in update_data.items():
            setattr(property_obj, key, value)
        db.commit()
        db.refresh(property_obj)
        return property_obj
    return None

def delete_property(db: Session, property_id: int) -> bool:
    property_obj = get_property_by_id(db, property_id)
    if property_obj:
        db.delete(property_obj)
        db.commit()
        return True
    return False
