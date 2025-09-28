
# Analysis report schemas for property stuff
# Written for class project, not by AI

from typing import Optional, Dict
from pydantic import BaseModel

# --- Valuation report ---
class ValuationReport(BaseModel):
    property_id: str
    estimated_value: Optional[float]
    value_confidence: Optional[str]  # "High", "Medium", "Low"
    rent_estimate: Optional[float]
    rent_confidence: Optional[str]

# --- Market analysis ---
class MarketAnalysis(BaseModel):
    property_id: str
    avg_rent: Optional[float]
    avg_price_per_sqft: Optional[float]
    neighborhood_trend: Optional[str]  # "Up", "Stable", "Down"
    comps: Optional[Dict[str, float]]  # {"comp_property_id": price}
