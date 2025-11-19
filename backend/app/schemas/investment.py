from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any


class ExpenseOverrides(BaseModel):
    # Rates as fractions (e.g., 0.10 = 10%)
    property_management_rate: Optional[float] = None
    maintenance_repairs_rate: Optional[float] = None
    vacancy_allowance_rate: Optional[float] = None
    insurance_rate: Optional[float] = None
    property_tax_rate: Optional[float] = None  # fallback rate if taxes_annual not provided and no DB tax data
    utilities_rate: Optional[float] = None     # fraction of annual rent; default is 0.0

    # Absolute annual overrides
    hoa_monthly: Optional[float] = None        # if provided, used (x12) instead of DB HOA
    hoa_annual: Optional[float] = None         # takes precedence over hoa_monthly
    taxes_annual: Optional[float] = None       # takes precedence over property_tax_rate fallback

class AddressAnalysisRequest(BaseModel):
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zip_code: str = Field(..., min_length=3, max_length=10, alias="zip")
    overrides: Optional[ExpenseOverrides] = None
    monthly_rent: Optional[float] = Field(None, alias="monthlyRent")

    @validator("street", "city", "state", "zip_code")
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field is required")
        return v.strip()

    class Config:
        populate_by_name = True


class InvestmentAnalysisResponse(BaseModel):
    cap_rate_percent: float
    recommendation: str
    explanation: str
    property_id: Optional[int] = None
    property_address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    report: Optional[str] = None
