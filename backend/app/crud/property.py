from sqlalchemy.orm import Session
from app.models.property import Property
from app.schemas.property_schemas import PropertyCreate, PropertyUpdate
from typing import Optional, List

def get_property_by_id(db: Session, property_id: int) -> Optional[Property]:
    return db.query(Property).filter(Property.id == property_id).first()

def get_all_properties(db: Session) -> List[Property]:
    return db.query(Property).all()

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
