from typing import Dict, Any, Optional
from datetime import date

# Heuristic-only, DB-data-only estimations. No external API calls.
# Intent: provide a reasonable cap rate estimate using property attributes on record.

DEFAULT_EXPENSE_RATES = {
    "property_management": 0.10,  # 10% of rent
    "maintenance_repairs": 0.08,  # 8% of rent
    "vacancy_allowance": 0.06,    # 6% of rent
    "insurance_rate": 0.007,      # 0.7% of property value per year
}

DEFAULT_PROPERTY_TAX_RATE = 0.013   # used only as a fallback when no tax data/override
DEFAULT_UTILITIES_RATE = 0.0        # as a fraction of annual rent

# Fallback per-sqft monthly rent baseline (very conservative). Adjusted by bedrooms/bathrooms.
BASE_RENT_PER_SQFT = 1.10
BEDROOM_BONUS = 150.0
BATHROOM_BONUS = 75.0

# Fallback price-per-sqft if value missing
FALLBACK_PRICE_PER_SQFT = 160.0


def _dict_get(d: Dict[str, Any] | None, *keys, default=None):
    cur = d or {}
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def estimate_monthly_rent(property_data: Dict[str, Any]) -> float:
    """Estimate monthly rent using only on-record attributes.

    Formula: sqft * base + bedroom/ba bonuses. Clamped minimally at 0.
    """
    sqft = float(property_data.get("squareFootage") or 0) or float(property_data.get("square_footage") or 0)
    beds = float(property_data.get("bedrooms") or 0)
    baths = float(property_data.get("bathrooms") or 0)

    base = sqft * BASE_RENT_PER_SQFT
    adj = (beds * BEDROOM_BONUS) + (baths * BATHROOM_BONUS)

    rent = max(0.0, base + adj)
    # Put a light lower/upper sanity clamp to avoid absurd values for tiny/huge entries
    if sqft and rent / max(1.0, sqft) < 0.6:
        rent = sqft * 0.6 + adj
    if sqft and rent / sqft > 3.5:
        rent = sqft * 3.5 + adj
    return round(rent, 2)


def get_property_value(property_data: Dict[str, Any]) -> float:
    """Use last sale price if available/recent; else fallback by sqft.
    We avoid any external estimates and keep calculation deterministic.
    """
    value = property_data.get("lastSalePrice") or property_data.get("last_sale_price")
    last_sale_date = property_data.get("lastSaleDate") or property_data.get("last_sale_date")

    # If there's no value at all, fallback by sqft
    if not value:
        sqft = float(property_data.get("squareFootage") or property_data.get("square_footage") or 0)
        if sqft > 0:
            return round(sqft * FALLBACK_PRICE_PER_SQFT, 2)
        return 0.0

    # If we have a value, just use it. We could age-adjust if very old, but
    # that would introduce additional assumptions; keep it simple.
    try:
        return float(value)
    except Exception:
        return 0.0


def _get_property_taxes_annual(property_data: Dict[str, Any], property_value: float, tax_rate_fallback: float) -> float:
    # propertyTaxes expected shape from DB mirrors RentCast: {"2023": {"total": 3200, ...}, ...}
    taxes = property_data.get("propertyTaxes") or property_data.get("property_taxes") or {}
    if isinstance(taxes, dict) and taxes:
        try:
            recent_year = max(taxes.keys(), key=lambda x: int(x))
            amt = _dict_get(taxes, recent_year, "total", default=None)
            if isinstance(amt, (int, float)) and amt > 0:
                return float(amt)
        except Exception:
            pass
    # If absent, estimate as provided fallback rate of value
    return float(property_value) * float(tax_rate_fallback)


def _get_hoa_annual(property_data: Dict[str, Any]) -> float:
    hoa = property_data.get("hoa") or {}
    monthly = _dict_get(hoa, "fee", default=0) or _dict_get(hoa, "monthlyFee", default=0)
    if isinstance(monthly, (int, float)) and monthly > 0:
        return float(monthly) * 12.0
    return 0.0


def _merge_rates(overrides: Optional[Dict[str, Any]]) -> Dict[str, float]:
    rates = {
        "property_management": DEFAULT_EXPENSE_RATES["property_management"],
        "maintenance_repairs": DEFAULT_EXPENSE_RATES["maintenance_repairs"],
        "vacancy_allowance": DEFAULT_EXPENSE_RATES["vacancy_allowance"],
        "insurance_rate": DEFAULT_EXPENSE_RATES["insurance_rate"],
        "property_tax_rate": DEFAULT_PROPERTY_TAX_RATE,
        "utilities_rate": DEFAULT_UTILITIES_RATE,
    }

    if overrides:
        # Map *_rate fields into internal names
        mapping = {
            "property_management_rate": "property_management",
            "maintenance_repairs_rate": "maintenance_repairs",
            "vacancy_allowance_rate": "vacancy_allowance",
            "insurance_rate": "insurance_rate",
            "property_tax_rate": "property_tax_rate",
            "utilities_rate": "utilities_rate",
        }
        for k_src, k_dst in mapping.items():
            if k_src in overrides and overrides[k_src] is not None:
                try:
                    rates[k_dst] = float(overrides[k_src])
                except Exception:
                    pass
    return rates


def compute_annual_expenses(
    property_data: Dict[str, Any],
    annual_rent: float,
    property_value: float,
    overrides: Optional[Dict[str, Any]] = None,
) -> float:
    """Compute annual operating expenses with optional user overrides.

    Overrides supported keys:
    - *_rate: property_management_rate, maintenance_repairs_rate, vacancy_allowance_rate,
              insurance_rate, property_tax_rate, utilities_rate
    - hoa_monthly, hoa_annual, taxes_annual
    """
    rates = _merge_rates(overrides)

    e = 0.0
    # Rent-based expenses
    e += annual_rent * rates["property_management"]
    e += annual_rent * rates["maintenance_repairs"]
    e += annual_rent * rates["vacancy_allowance"]
    e += annual_rent * rates["utilities_rate"]

    # Value-based expenses
    e += property_value * rates["insurance_rate"]

    # Taxes (annual): explicit override > DB data > fallback rate
    taxes_annual = None
    if overrides and overrides.get("taxes_annual") is not None:
        try:
            taxes_annual = float(overrides.get("taxes_annual"))
        except Exception:
            taxes_annual = None
    if taxes_annual is None:
        taxes_annual = _get_property_taxes_annual(property_data, property_value, rates["property_tax_rate"])
    e += taxes_annual

    # HOA (annual): explicit override > DB-derived
    hoa_annual = None
    if overrides:
        if overrides.get("hoa_annual") is not None:
            try:
                hoa_annual = float(overrides.get("hoa_annual"))
            except Exception:
                hoa_annual = None
        elif overrides.get("hoa_monthly") is not None:
            try:
                hoa_annual = float(overrides.get("hoa_monthly")) * 12.0
            except Exception:
                hoa_annual = None
    if hoa_annual is None:
        hoa_annual = _get_hoa_annual(property_data)
    e += hoa_annual

    return e


def analyze_investment(
    property_data: Dict[str, Any],
    overrides: Optional[Dict[str, Any]] = None,
    monthly_rent_override: Optional[float] = None,
) -> Dict[str, Any]:
    """Return cap rate and recommendation using only DB data.

    Response keys:
    - cap_rate_percent: float
    - recommendation: str ("Worth investing" | "Maybe" | "Not worth it")
    - explanation: str
    - details: Dict for debugging/visibility
    """
    value = get_property_value(property_data)
    if value <= 0:
        return {
            "cap_rate_percent": 0.0,
            "recommendation": "Not worth it",
            "explanation": "Unable to determine property value from database records.",
            "details": {"value": value}
        }

    # Use provided monthly rent if given; otherwise estimate from DB fields
    if monthly_rent_override is not None and monthly_rent_override > 0:
        monthly_rent = float(monthly_rent_override)
    else:
        monthly_rent = estimate_monthly_rent(property_data)
    if monthly_rent <= 0:
        return {
            "cap_rate_percent": 0.0,
            "recommendation": "Not worth it",
            "explanation": "Missing rent drivers (sqft/bed/bath); cannot estimate income from DB-only data.",
            "details": {"value": value, "monthly_rent": monthly_rent}
        }

    annual_rent = monthly_rent * 12.0
    expenses = compute_annual_expenses(property_data, annual_rent, value, overrides=overrides)
    noi = max(0.0, annual_rent - expenses)
    cap_rate = (noi / value) * 100.0 if value > 0 else 0.0
    cap_rate = round(cap_rate, 2)

    # Simple rule-based recommendation
    if cap_rate >= 8.0:
        rec = "Worth investing"
        note = f"Cap rate {cap_rate}% meets or exceeds the 8% target."
    elif cap_rate >= 6.0:
        rec = "Maybe"
        note = f"Cap rate {cap_rate}% is borderline; consider negotiating price or reducing expenses."
    else:
        rec = "Not worth it"
        note = f"Cap rate {cap_rate}% is below a typical 6–8% target range."

    return {
        "cap_rate_percent": cap_rate,
        "recommendation": rec,
        "explanation": note,
        "details": {
            "value": round(value, 2),
            "monthly_rent": round(monthly_rent, 2),
            "annual_rent": round(annual_rent, 2),
            "annual_expenses": round(expenses, 2),
            "noi": round(noi, 2)
        }
    }


def generate_investment_report(property_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Create a narrative investment report blending property characteristics and financial metrics.

    The tone is professional and explanatory; numbers are contextualized and actionable insights highlighted.
    """
    # Extract address components
    line1 = property_data.get("addressLine1") or property_data.get("address_line1") or "(Street Unknown)"
    city = property_data.get("city") or ""
    state = property_data.get("state") or ""
    zip_code = property_data.get("zipCode") or property_data.get("zip_code") or ""
    formatted_address = property_data.get("formattedAddress") or property_data.get("formatted_address")

    bedrooms = property_data.get("bedrooms")
    bathrooms = property_data.get("bathrooms")
    sqft = property_data.get("squareFootage") or property_data.get("square_footage")
    year_built = property_data.get("yearBuilt") or property_data.get("year_built")
    property_type = property_data.get("propertyType") or property_data.get("property_type")

    cap_rate = analysis.get("cap_rate_percent", 0.0)
    rec = analysis.get("recommendation", "")
    details = analysis.get("details", {})
    value = details.get("value")
    monthly_rent = details.get("monthly_rent")
    annual_rent = details.get("annual_rent")
    annual_expenses = details.get("annual_expenses")
    noi = details.get("noi")

    # Derived ratios
    expense_ratio = (annual_expenses / annual_rent) if annual_rent else None
    rent_to_value = (annual_rent / value) if (annual_rent and value) else None

    strengths = []
    weaknesses = []

    if cap_rate >= 8:
        strengths.append("Cap rate meets or exceeds typical target benchmark (≥8%).")
    elif cap_rate >= 6:
        strengths.append("Cap rate is within a negotiable range; could be improved with pricing or expense optimization.")
    else:
        weaknesses.append("Cap rate is below the desirable 6–8% range, reducing attractiveness for standard buy-and-hold investors.")

    if expense_ratio is not None:
        if expense_ratio < 0.40:
            strengths.append("Operating expenses consume a reasonable share of gross rent (<40%).")
        elif expense_ratio > 0.55:
            weaknesses.append("Operating expenses are elevated (>55% of gross rent), compressing net operating income.")

    if rent_to_value is not None:
        if rent_to_value >= 0.09:
            strengths.append("Gross rent relative to property value is strong, supporting returns.")
        elif rent_to_value < 0.06:
            weaknesses.append("Gross rent is low compared to property value, which may hinder yield unless price adjusts.")

    if sqft and bedrooms:
        if bedrooms and sqft and sqft / bedrooms < 500:
            weaknesses.append("Bedroom-to-square-footage ratio indicates smaller bedroom sizes; could affect tenant appeal.")
        elif bedrooms and sqft and sqft / bedrooms > 800:
            strengths.append("Generous square footage per bedroom; potential for premium positioning or multi-use space.")

    if year_built:
        if year_built >= 2005:
            strengths.append("Relatively modern construction year may reduce near-term capital expenditure risk.")
        elif year_built < 1980:
            weaknesses.append("Older construction could imply higher future maintenance or capex requirements.")

    if property_type:
        if str(property_type).lower() in {"single family", "single_family", "single-family"}:
            strengths.append("Single-family property often benefits from stable tenant demand and simpler management.")

    # Start building report sections
    title_line = formatted_address or f"{line1}, {city}, {state} {zip_code}".strip()

    summary_parts = [
        f"Property Investment Analysis Report",
        f"Subject Property: {title_line}",
    ]
    if property_type:
        summary_parts.append(f"Type: {property_type}")
    if bedrooms is not None or bathrooms is not None:
        summary_parts.append(f"Configuration: {bedrooms or 'N/A'} BR / {bathrooms or 'N/A'} BA")
    if sqft:
        summary_parts.append(f"Approximate Size: {sqft} sq ft")
    if year_built:
        summary_parts.append(f"Year Built: {year_built}")

    summary_section = "\n".join(summary_parts)

    metrics_section = (
        "Key Financial Metrics:\n"
        f"  Estimated Value: ${value:,.0f}\n"
        f"  Estimated Monthly Rent: ${monthly_rent:,.0f}\n"
        f"  Estimated Annual Rent: ${annual_rent:,.0f}\n"
        f"  Estimated Annual Operating Expenses: ${annual_expenses:,.0f}\n"
        f"  Net Operating Income (NOI): ${noi:,.0f}\n"
        f"  Cap Rate: {cap_rate:.2f}%\n"
    )

    cap_rate_explainer = (
        "Cap Rate Context:\n"
        f"  The cap rate of {cap_rate:.2f}% represents the unlevered annual return based on current income and expenses. "
        "It is calculated as Net Operating Income divided by Property Value. "
        "In many markets, stabilized residential rental investments target cap rates in the ~6–8% range. "
        f"This property's cap rate suggests: {rec}."
    )

    if expense_ratio is not None and rent_to_value is not None:
        cap_rate_explainer += (
            f"\n  Expense Ratio (OpEx / Gross Rent): {expense_ratio*100:.1f}% — "
            + ("efficient relative to typical 40–50% ranges." if expense_ratio < 0.40 else
               "moderate and should be monitored." if expense_ratio <= 0.55 else
               "high; investigate tax burden, insurance, or maintenance line items.")
            + f"\n  Gross Rent-to-Value Ratio: {rent_to_value*100:.2f}% — "
            + ("supports the income basis for valuation." if rent_to_value >= 0.09 else
               "may limit return potential unless rent growth or price adjustment occurs.")
        )

    strengths_section = "Strengths:\n  - " + "\n  - ".join(strengths) if strengths else "Strengths:\n  - No pronounced strengths identified from available data."
    weaknesses_section = "Weaknesses / Watch Items:\n  - " + "\n  - ".join(weaknesses) if weaknesses else "Weaknesses / Watch Items:\n  - No critical weaknesses surfaced; still perform onsite due diligence."

    action_items = []
    if rec == "Worth investing":
        action_items.append("Proceed to detailed due diligence: inspection, rent comparables, and verify tax history.")
    elif rec == "Maybe":
        action_items.append("Model scenarios with negotiated purchase price or targeted expense reductions.")
        action_items.append("Order a professional rent comp analysis to validate income assumptions.")
    else:
        action_items.append("Reassess pricing or identify operational improvements before acquisition.")
        action_items.append("Analysis alternative assets with stronger NOI yield.")

    action_section = "Recommended Next Steps:\n  - " + "\n  - ".join(action_items)

    report = (
        f"{summary_section}\n\n"
        f"{metrics_section}\n"
        f"{cap_rate_explainer}\n\n"
        f"{strengths_section}\n\n"
        f"{weaknesses_section}\n\n"
        f"{action_section}"
    )

    return report
