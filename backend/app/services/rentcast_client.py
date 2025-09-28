import requests
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings


class RentCastClient:
    BASE_URL = "https://api.rentcast.io/v1"
    RATE_LIMIT_FILE = "rentcast_api_calls.json"
    MAX_MONTHLY_CALLS = 50

    def __init__(self):
        self.api_key = settings.RENTCAST_API_KEY
        self.headers = {"X-Api-Key": self.api_key}

    def _load_rate_limit_data(self) -> Dict[str, Any]:
        """Load rate limiting data from file"""
        try:
            if os.path.exists(self.RATE_LIMIT_FILE):
                with open(self.RATE_LIMIT_FILE, 'r') as f:
                    data = json.load(f)
                # Reset counter if new month
                current_month = datetime.now().strftime("%Y-%m")
                if data.get("month") != current_month:
                    data = {"month": current_month, "calls": 0}
                return data
        except:
            pass
        return {"month": datetime.now().strftime("%Y-%m"), "calls": 0}

    def _save_rate_limit_data(self, data: Dict[str, Any]):
        """Save rate limiting data to file"""
        try:
            with open(self.RATE_LIMIT_FILE, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def _check_rate_limit(self) -> bool:
        """Check if we can make another API call"""
        data = self._load_rate_limit_data()
        return data["calls"] < self.MAX_MONTHLY_CALLS

    def _increment_call_count(self):
        """Increment the API call counter"""
        data = self._load_rate_limit_data()
        data["calls"] += 1
        self._save_rate_limit_data(data)

    def get_rent_estimate(self, property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get rent estimate from RentCast API"""
        if not self._check_rate_limit():
            raise Exception(f"Monthly API limit of {self.MAX_MONTHLY_CALLS} calls reached")

        url = f"{self.BASE_URL}/avm/rent/long-term"
        params = {
            "address": property_data.get("formattedAddress"),
            "propertyType": property_data.get("propertyType"),
            "bedrooms": property_data.get("bedrooms"),
            "bathrooms": property_data.get("bathrooms"),
            "squareFootage": property_data.get("squareFootage"),
            "compCount": 5
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            self._increment_call_count()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"RentCast API error: {str(e)}")

    def get_property_value(self, property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get property value estimate from RentCast API (fallback when lastSalePrice is too old)"""
        if not self._check_rate_limit():
            raise Exception(f"Monthly API limit of {self.MAX_MONTHLY_CALLS} calls reached")

        url = f"{self.BASE_URL}/avm/value"
        params = {
            "address": property_data.get("formattedAddress"),
            "propertyType": property_data.get("propertyType"),
            "bedrooms": property_data.get("bedrooms"),
            "bathrooms": property_data.get("bathrooms"),
            "squareFootage": property_data.get("squareFootage")
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            self._increment_call_count()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"RentCast API error: {str(e)}")

    def get_remaining_calls(self) -> int:
        """Get remaining API calls for this month"""
        data = self._load_rate_limit_data()
        return max(0, self.MAX_MONTHLY_CALLS - data["calls"])