import requests
from typing import Optional, Dict

RENTCAST_API_URL = "https://api.rentcast.io/v1/properties"
RENTCAST_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual RentCast API key

def get_property_data(address: str) -> Optional[Dict]:
	"""
	Fetch property data from RentCast API for a given address.
	Returns a dictionary with property data if successful, else None.
	"""
	headers = {
		"X-Api-Key": RENTCAST_API_KEY
	}
	params = {
		"address": address
	}
	response = requests.get(RENTCAST_API_URL, headers=headers, params=params)
	response.raise_for_status()
	return response.json()

