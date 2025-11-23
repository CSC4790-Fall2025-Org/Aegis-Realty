from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from app.services.rentcast_client import RentCastClient
from .rent_estimation import RentEstimator


class PropertyAnalyzer:
    def __init__(self):
        self.rentcast_client = RentCastClient()
        self.rent_estimator = RentEstimator()

        # Default expense percentages (as % of gross rent)
        self.DEFAULT_EXPENSES = {
            "property_management": 0.10,  # 10% - Property management fees
            "maintenance_repairs": 0.08,  # 8% - Maintenance and repairs
            "vacancy_allowance": 0.06,  # 6% - Vacancy allowance
            "insurance_rate": 0.007,  # 0.7% of property value annually
            "property_tax_rate": 0.015  # 1.5% of property value annually (fallback)
        }

    def analyze_property(self, property_data: Dict[str, Any],
                         calculation_mode: str = "gross",
                         custom_expenses: Optional[Dict[str, float]] = None,
                         cap_rate_threshold: float = 8.0) -> Dict[str, Any]:
        """
        Main orchestration function for property analysis

        Args:
            property_data: Property information from database
            calculation_mode: "gross" or "net" - how to calculate cap rate
            custom_expenses: Optional custom expense percentages
            cap_rate_threshold: Minimum acceptable cap rate (default 8%)
        """

        # Merge custom expenses with defaults
        expenses = {**self.DEFAULT_EXPENSES}
        if custom_expenses:
            expenses.update(custom_expenses)

        # Get rent estimate
        rent_data = self._get_rent_estimate(property_data)

        # Get property value
        property_value = self._get_property_value(property_data)

        # Calculate cap rates
        cap_rates = self._calculate_cap_rates(
            rent_data, property_value, property_data,
            calculation_mode, expenses
        )

        # Generate analysis results
        analysis = {
            "property_value": property_value,
            "rent_estimates": rent_data,
            "cap_rates": cap_rates,
            "expenses_used": expenses,
            "calculation_mode": calculation_mode,
            "meets_threshold": self._meets_investment_threshold(cap_rates, cap_rate_threshold),
            "recommendation": self._generate_recommendation(cap_rates, cap_rate_threshold),
            "api_calls_remaining": self.rentcast_client.get_remaining_calls()
        }

        return analysis

    def _get_rent_estimate(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get rent estimate from RentCast API or internal calculation"""
        try:
            # Try RentCast API first
            rent_data = self.rentcast_client.get_rent_estimate(property_data)
            return {
                "source": "rentcast_api",
                "rent": rent_data.get("rent", 0),
                "rent_low": rent_data.get("rentRangeLow", 0),
                "rent_high": rent_data.get("rentRangeHigh", 0),
                "comparables": rent_data.get("comparables", [])
            }
        except Exception as e:
            print(f"RentCast API failed, using internal estimation: {str(e)}")
            # Fallback to internal estimation (would need property database query here)
            # For now, return placeholder - this would be implemented with database access
            return {
                "source": "internal_estimate",
                "rent": 0,
                "rent_low": 0,
                "rent_high": 0,
                "comparables": [],
                "error": str(e)
            }

    def _get_property_value(self, property_data: Dict[str, Any]) -> float:
        """Get property value - use last sale price or API estimate"""
        last_sale_price = property_data.get("lastSalePrice")
        last_sale_date = property_data.get("lastSaleDate")

        # Check if last sale price is recent enough (within 10 years)
        if last_sale_price and last_sale_date:
            try:
                sale_date = datetime.fromisoformat(last_sale_date.replace('Z', '+00:00'))
                years_ago = (datetime.now() - sale_date.replace(tzinfo=None)).days / 365.25

                if years_ago <= 10:
                    return last_sale_price
            except:
                pass

        # Fallback to RentCast value API
        try:
            value_data = self.rentcast_client.get_property_value(property_data)
            return value_data.get("value", last_sale_price or 0)
        except Exception as e:
            print(f"Could not get updated property value: {str(e)}")
            return last_sale_price or 0

    def _calculate_cap_rates(self, rent_data: Dict[str, Any], property_value: float,
                             property_data: Dict[str, Any], calculation_mode: str,
                             expenses: Dict[str, float]) -> Dict[str, Any]:
        """Calculate cap rates for rent range"""

        if property_value <= 0:
            return {"error": "Invalid property value"}

        rent_scenarios = {
            "low": rent_data.get("rent_low", 0),
            "mid": rent_data.get("rent", 0),
            "high": rent_data.get("rent_high", 0)
        }

        cap_rates = {}

        for scenario, monthly_rent in rent_scenarios.items():
            if monthly_rent <= 0:
                cap_rates[scenario] = 0
                continue

            annual_rent = monthly_rent * 12

            if calculation_mode == "gross":
                # Gross cap rate: annual rent / property value
                cap_rate = (annual_rent / property_value) * 100
            else:
                # Net cap rate: (annual rent - expenses) / property value
                annual_expenses = self._calculate_annual_expenses(
                    annual_rent, property_value, property_data, expenses
                )
                net_income = annual_rent - annual_expenses
                cap_rate = (net_income / property_value) * 100

            cap_rates[scenario] = round(cap_rate, 2)

        return cap_rates

    def _calculate_annual_expenses(self, annual_rent: float, property_value: float,
                                   property_data: Dict[str, Any],
                                   expense_rates: Dict[str, float]) -> float:
        """Calculate total annual expenses"""

        expenses = 0

        # Percentage of rent expenses
        expenses += annual_rent * expense_rates.get("property_management", 0)
        expenses += annual_rent * expense_rates.get("maintenance_repairs", 0)
        expenses += annual_rent * expense_rates.get("vacancy_allowance", 0)

        # Property value based expenses
        expenses += property_value * expense_rates.get("insurance_rate", 0)

        # Property taxes - use actual if available, otherwise estimate
        property_taxes = self._get_property_taxes(property_data, property_value, expense_rates)
        expenses += property_taxes

        # HOA fees if applicable (annual)
        hoa_fee = property_data.get("hoa", {}).get("fee", 0)
        if hoa_fee:
            expenses += hoa_fee * 12  # Convert monthly to annual

        return expenses

    def _get_property_taxes(self, property_data: Dict[str, Any],
                            property_value: float, expense_rates: Dict[str, float]) -> float:
        """Get property taxes from data or estimate"""

        # Try to get most recent tax data
        property_taxes = property_data.get("propertyTaxes", {})
        if property_taxes:
            # Get most recent year's taxes
            recent_year = max(property_taxes.keys(), key=lambda x: int(x))
            tax_amount = property_taxes[recent_year].get("total", 0)
            if tax_amount:
                return tax_amount

        # Fallback to percentage estimate
        return property_value * expense_rates.get("property_tax_rate", 0.015)

    def _meets_investment_threshold(self, cap_rates: Dict[str, Any],
                                    threshold: float) -> Dict[str, bool]:
        """Check if property meets investment threshold"""
        if "error" in cap_rates:
            return {"low": False, "mid": False, "high": False}

        return {
            scenario: cap_rate >= threshold
            for scenario, cap_rate in cap_rates.items()
        }

    def _generate_recommendation(self, cap_rates: Dict[str, Any],
                                 threshold: float) -> Dict[str, Any]:
        """Generate investment recommendation"""

        if "error" in cap_rates:
            return {
                "decision": "Cannot Analysis",
                "reason": "Insufficient data for analysis"
            }

        mid_cap_rate = cap_rates.get("mid", 0)

        if mid_cap_rate >= threshold:
            return {
                "decision": "Invest",
                "reason": f"Cap rate of {mid_cap_rate}% meets minimum threshold of {threshold}%"
            }
        elif mid_cap_rate >= threshold * 0.8:  # Within 20% of threshold
            return {
                "decision": "Consider",
                "reason": f"Cap rate of {mid_cap_rate}% is close to threshold. Consider negotiating price."
            }
        else:
            return {
                "decision": "Do Not Invest",
                "reason": f"Cap rate of {mid_cap_rate}% is below minimum threshold of {threshold}%"
            }