from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import date
from typing import Any

class PropertyRecord(BaseModel):
    id: int
    formatted_address: Optional[str] = Field(None, alias="formattedAddress")
    address_line1: Optional[str] = Field(None, alias="addressLine1")
    address_line2: Optional[str] = Field(None, alias="addressLine2")
    city: Optional[str] = None
    state: Optional[str] = None
    state_fips: Optional[str] = Field(None, alias="stateFips")
    zip_code: Optional[str] = Field(None, alias="zipCode")
    county: Optional[str] = None
    county_fips: Optional[str] = Field(None, alias="countyFips")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_type: Optional[str] = Field(None, alias="propertyType")
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_footage: Optional[int] = Field(None, alias="squareFootage")
    lot_size: Optional[int] = Field(None, alias="lotSize")
    year_built: Optional[int] = Field(None, alias="yearBuilt")
    assessor_id: Optional[str] = Field(None, alias="assessorID")
    subdivision: Optional[str] = None
    zoning: Optional[str] = None
    last_sale_date: Optional[date] = Field(None, alias="lastSaleDate")  # match SQLAlchemy Date
    last_sale_price: Optional[float] = Field(None, alias="lastSalePrice")
    owner_occupied: Optional[bool] = Field(None, alias="ownerOccupied")

    # JSON fields in SQLAlchemy 
    features: Optional[Dict[str, Any]] = None
    hoa: Optional[Dict[str, Any]] = None
    owners: Optional[Any] = None
    tax_assessments: Optional[Dict[str, Any]] = Field(None, alias="taxAssessments")
    property_taxes: Optional[Dict[str, Any]] = Field(None, alias="propertyTaxes")
    sale_history: Optional[Dict[str, Any]] = Field(None, alias="saleHistory")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        allow_population_by_alias = True

class PropertyAnalysisRequest(BaseModel):
    address: str
    calculation_mode: Optional[str] = "gross"  # 'gross' or 'net'
    custom_expenses: Optional[Dict[str, Any]] = None
    cap_rate_threshold: Optional[float] = 8.0


class PropertyAnalysisResponse(BaseModel):
    property_data: Optional[PropertyRecord]
    financial_analysis: Optional[Dict[str, Any]]
    ai_analysis: Optional[Dict[str, Any]]
    success: bool = False
    message: Optional[str] = None
