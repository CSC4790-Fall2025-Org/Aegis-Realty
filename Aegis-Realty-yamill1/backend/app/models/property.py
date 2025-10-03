from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"
    id = Column(String, primary_key=True, index=True)
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
    legal_description = Column(String)
    subdivision = Column(String)
    zoning = Column(String)
    last_sale_date = Column(Date)
    last_sale_price = Column(Float)
    owner_occupied = Column(Boolean)

    features = relationship("Features", back_populates="property", uselist=False)
    hoa = relationship("HOA", back_populates="property", uselist=False)
    owners = relationship("Owner", back_populates="property")
    tax_assessments = relationship("TaxAssessment", back_populates="property")
    property_taxes = relationship("PropertyTax", back_populates="property")
    sale_history = relationship("SaleHistory", back_populates="property")

class Features(Base):
    __tablename__ = "features"
    property_id = Column(String, ForeignKey("properties.id"), primary_key=True)
    data = Column(JSON)
    property = relationship("Property", back_populates="features")

class HOA(Base):
    __tablename__ = "hoa"
    property_id = Column(String, ForeignKey("properties.id"), primary_key=True)
    data = Column(JSON)
    property = relationship("Property", back_populates="hoa")

class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(String, ForeignKey("properties.id"))
    data = Column(JSON)
    property = relationship("Property", back_populates="owners")

class TaxAssessment(Base):
    __tablename__ = "tax_assessments"
    property_id = Column(String, ForeignKey("properties.id"), primary_key=True)
    year = Column(Integer, primary_key=True)
    data = Column(JSON)
    property = relationship("Property", back_populates="tax_assessments")

class PropertyTax(Base):
    __tablename__ = "property_taxes"
    property_id = Column(String, ForeignKey("properties.id"), primary_key=True)
    year = Column(Integer, primary_key=True)
    data = Column(JSON)
    property = relationship("Property", back_populates="property_taxes")

class SaleHistory(Base):
    __tablename__ = "sale_history"
    property_id = Column(String, ForeignKey("properties.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    data = Column(JSON)
    property = relationship("Property", back_populates="sale_history")
