from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Property(Base):
    #create sepepreate for favortites (user proeprties) 
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    formatted_address = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    state_fips = Column(String)
    zip_code = Column(String)
    county = Column(String)
    county_fips = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    property_type = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_footage = Column(Integer) 
    lot_size = Column(Integer)
    year_built = Column(Integer)
    assessor_id = Column(String)
    subdivision = Column(String)
    zoning = Column(String)
    last_sale_date = Column(Date)
    last_sale_price = Column(Float)
    owner_occupied = Column(Boolean)
    features = Column(JSON, nullable=True)
    hoa = Column(JSON, nullable=True)
    owners = Column(JSON, nullable=True)
    tax_assessments = Column(JSON, nullable=True)
    property_taxes = Column(JSON, nullable=True)
    sale_history = Column(JSON, nullable=True)


