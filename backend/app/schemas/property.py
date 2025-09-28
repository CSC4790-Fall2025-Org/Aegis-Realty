from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class MailingAddress(BaseModel):
    id: Optional[str]
    formattedAddress: Optional[str]
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    stateFips: Optional[str]
    zipCode: Optional[str]

class Owner(BaseModel):
    names: Optional[List[str]]
    type: Optional[str]
    mailingAddress: Optional[MailingAddress]

class TaxAssessment(BaseModel):
    year: int
    value: Optional[float]
    land: Optional[float]
    improvements: Optional[float]

class PropertyTax(BaseModel):
    year: int
    total: Optional[float]

class SaleHistory(BaseModel):
    event: str
    date: str
    price: Optional[float]

class HOA(BaseModel):
    fee: Optional[float]

class Features(BaseModel):
    architectureType: Optional[str]
    cooling: Optional[bool]
    coolingType: Optional[str]
    exteriorType: Optional[str]
    fireplace: Optional[bool]
    fireplaceType: Optional[str]
    floorCount: Optional[int]
    foundationType: Optional[str]
    garage: Optional[bool]
    garageSpaces: Optional[int]
    garageType: Optional[str]
    heating: Optional[bool]
    heatingType: Optional[str]
    pool: Optional[bool]
    poolType: Optional[str]
    roofType: Optional[str]
    roomCount: Optional[int]
    unitCount: Optional[int]
    viewType: Optional[str]

class PropertyRecord(BaseModel):
    id: str
    formattedAddress: Optional[str]
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    stateFips: Optional[str]
    zipCode: Optional[str]
    county: Optional[str]
    countyFips: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    propertyType: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[float]
    squareFootage: Optional[int]
    lotSize: Optional[int]
    yearBuilt: Optional[int]
    assessorID: Optional[str]
    legalDescription: Optional[str]
    subdivision: Optional[str]
    zoning: Optional[str]
    lastSaleDate: Optional[str]
    lastSalePrice: Optional[float]
    hoa: Optional[HOA]
    features: Optional[Features]
    taxAssessments: Optional[Dict[str, TaxAssessment]]
    propertyTaxes: Optional[Dict[str, PropertyTax]]
    history: Optional[Dict[str, SaleHistory]]
    owner: Optional[Owner]
    ownerOccupied: Optional[bool]
    roomCount: Optional[int]
    unitCount: Optional[int]
    viewType: Optional[str]

class PropertyRecord(BaseModel):
    id: str
    formattedAddress: Optional[str]
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    stateFips: Optional[str]
    zipCode: Optional[str]
    county: Optional[str]
    countyFips: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    propertyType: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[float]
    squareFootage: Optional[int]
    lotSize: Optional[int]
    yearBuilt: Optional[int]
    assessorID: Optional[str]
    legalDescription: Optional[str]
    subdivision: Optional[str]
    zoning: Optional[str]
    lastSaleDate: Optional[str]
    lastSalePrice: Optional[float]
    hoa: Optional[HOA]
    features: Optional[Features]
    taxAssessments: Optional[Dict[str, TaxAssessment]]
    propertyTaxes: Optional[Dict[str, PropertyTax]]
    history: Optional[Dict[str, SaleHistory]]
    owner: Optional[Owner]
    ownerOccupied: Optional[bool]

class PropertyAnalysisRequest(BaseModel):
    address: str
    calculation_mode: Optional[str] = "gross"
    cap_rate_threshold: Optional[float] = 8.0
    custom_expenses: Optional[Dict[str, float]] = None

class PropertyAnalysisResponse(BaseModel):
    property_data: PropertyRecord
    financial_analysis: Dict[str, Any]
    ai_analysis: Dict[str, Any]
    success: bool
    message: str
