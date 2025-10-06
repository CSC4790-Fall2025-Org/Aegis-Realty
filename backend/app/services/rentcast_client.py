import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.core.config import settings

class RentCastClient:
    def __init__(self):
        self.api_key = settings.RENTCAST_API_KEY
        self.BASE_URL = "https://api.rentcast.io/v1"
        self.headers = {"X-Api-Key": self.api_key}

        # Rate limiting
        self.MAX_MONTHLY_CALLS = 50
        self.rate_limit_file = "rentcast_rate_limit.json"

    def _check_rate_limit(self) -> bool:
        data = self._load_rate_limit_data()
        return data["calls"] < self.MAX_MONTHLY_CALLS

    def _load_rate_limit_data(self) -> Dict[str, Any]:
        if os.path.exists(self.rate_limit_file):
            with open(self.rate_limit_file, 'r') as f:
                data = json.load(f)
                # Reset if new month
                if data.get("month") != datetime.now().strftime("%Y-%m"):
                    data = {"month": datetime.now().strftime("%Y-%m"), "calls": 0}
        else:
            data = {"month": datetime.now().strftime("%Y-%m"), "calls": 0}
        return data

    def _save_rate_limit_data(self, data: Dict[str, Any]):
        """Save rate limit data to file"""
        with open(self.rate_limit_file, 'w') as f:
            json.dump(data, f)

    def _increment_call_count(self):
        """Increment API call counter"""
        data = self._load_rate_limit_data()
        data["calls"] += 1
        self._save_rate_limit_data(data)

    def get_random_properties(self, limit: int = 100) -> List[Dict[str, Any]]:
        if not self._check_rate_limit():
            raise Exception("Monthly API call limit exceeded")

        if limit < 1 or limit > 500:
            raise ValueError("Limit must be between 1 and 500")

        url = f"{self.BASE_URL}/properties/random"
        params = {"limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            self._increment_call_count()

            data = response.json()
            return data if isinstance(data, list) else data.get("properties", [])

        except requests.exceptions.RequestException as e:
            raise Exception(f"RentCast API error: {str(e)}")

    def get_rent_estimate(self, property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self._check_rate_limit():
            raise Exception("Monthly API call limit exceeded")

        url = f"{self.BASE_URL}/avm/rent/long-term"
        params = {
            "address": property_data.get("formattedAddress"),
            "city": property_data.get("city"),
            "state": property_data.get("state"),
            "zipCode": property_data.get("zipCode"),
            "bedrooms": property_data.get("bedrooms"),
            "bathrooms": property_data.get("bathrooms"),
            "squareFootage": property_data.get("squareFootage"),
            "propertyType": property_data.get("propertyType")
        }

        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            self._increment_call_count()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"RentCast API error: {str(e)}")

    def get_property_value(self, property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self._check_rate_limit():
            raise Exception("Monthly API call limit exceeded")

        url = f"{self.BASE_URL}/avm/value"
        params = {
            "address": property_data.get("formattedAddress"),
            "city": property_data.get("city"),
            "state": property_data.get("state"),
            "zipCode": property_data.get("zipCode"),
            "bedrooms": property_data.get("bedrooms"),
            "bathrooms": property_data.get("bathrooms"),
            "squareFootage": property_data.get("squareFootage"),
            "propertyType": property_data.get("propertyType")
        }

        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            self._increment_call_count()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"RentCast API error: {str(e)}")

    def get_remaining_calls(self) -> int:
        data = self._load_rate_limit_data()
        return max(0, self.MAX_MONTHLY_CALLS - data["calls"])