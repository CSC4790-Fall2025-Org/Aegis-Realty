import sys
import os
import requests
import json
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.models.property import Property
from app.core.config import settings

# Add the backend directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class RentCastPropertyLoader:
    def __init__(self):
        self.api_key = settings.RENTCAST_API_KEY
        self.BASE_URL = "https://api.rentcast.io/v1"

        if not self.api_key:
            raise ValueError("RENTCAST_API_KEY not found in settings")

        print(f"🔑 API Key configured: {self.api_key[:8]}...{self.api_key[-4:] if len(self.api_key) > 12 else 'short'}")

    def fetch_random_properties(self, count: int = 100) -> list:
        all_properties = []

        batch_size = min(500, count)
        remaining = count

        while remaining > 0:
            current_batch = min(batch_size, remaining)
            print(f"🔍 Fetching {current_batch} properties from RentCast API...")

            url = f"{self.BASE_URL}/properties/random"
            headers = {"X-Api-Key": self.api_key}
            params = {"limit": current_batch}

            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)

                print(f"📡 Response status: {response.status_code}")
                print(f"📡 Response headers: {dict(response.headers)}")

                if response.status_code == 401:
                    print("❌ Authentication failed. Check your API key.")
                    print(f"🔑 Using API key: {self.api_key[:8]}...{self.api_key[-4:]}")
                    return []

                response.raise_for_status()

                data = response.json()

                if isinstance(data, list):
                    properties = data
                elif isinstance(data, dict) and 'properties' in data:
                    properties = data['properties']
                else:
                    properties = [data] if data else []

                print(f"✅ Received {len(properties)} properties")
                all_properties.extend(properties)
                remaining -= len(properties)

                if len(properties) < current_batch:
                    print(f"⚠️ Received fewer properties than requested, stopping")
                    break

            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching random properties: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"📡 Response content: {e.response.text}")
                break

        return all_properties

    def create_property_from_api_data(self, prop_data: dict, db: Session) -> Optional[Property]:
        try:
            last_sale_date = None
            if prop_data.get("lastSaleDate"):
                try:
                    # Parse ISO date string to Python date
                    date_str = prop_data["lastSaleDate"]
                    if date_str.endswith('Z'):
                        date_str = date_str[:-1]
                    dt = datetime.fromisoformat(date_str.split('T')[0])
                    last_sale_date = dt.date()
                except Exception as e:
                    print(f"⚠️ Date parsing error: {e}")

            property_dict = {
                "formatted_address": prop_data.get("formattedAddress"),
                "address_line1": prop_data.get("addressLine1"),
                "address_line2": prop_data.get("addressLine2"),
                "city": prop_data.get("city"),
                "state": prop_data.get("state"),
                "state_fips": prop_data.get("stateFips"),
                "zip_code": prop_data.get("zipCode"),
                "county": prop_data.get("county"),
                "county_fips": prop_data.get("countyFips"),
                "latitude": prop_data.get("latitude"),
                "longitude": prop_data.get("longitude"),
                "property_type": prop_data.get("propertyType"),
                "bedrooms": prop_data.get("bedrooms"),
                "bathrooms": prop_data.get("bathrooms"),
                "square_footage": prop_data.get("squareFootage"),
                "lot_size": prop_data.get("lotSize"),
                "year_built": prop_data.get("yearBuilt"),
                "assessor_id": prop_data.get("assessorID"),
                "legal_description": prop_data.get("legalDescription"),
                "subdivision": prop_data.get("subdivision"),
                "zoning": prop_data.get("zoning"),
                "last_sale_date": last_sale_date,
                "last_sale_price": prop_data.get("lastSalePrice"),
                "owner_occupied": prop_data.get("ownerOccupied"),
                "features": prop_data.get("features"),
                "hoa": prop_data.get("hoa"),
                "owners": prop_data.get("owner"),
                "tax_assessments": prop_data.get("taxAssessments"),
                "property_taxes": prop_data.get("propertyTaxes"),
                "sale_history": prop_data.get("history")
            }

            property_dict = {k: v for k, v in property_dict.items() if v is not None}

            return Property(**property_dict)

        except Exception as e:
            print(f"❌ Error creating property: {str(e)}")
            print(f"📋 Property data: {json.dumps(prop_data, indent=2, default=str)}")
            return None

    def load_properties_to_database(self, properties: list) -> int:
        if not properties:
            print("❌ No properties to load")
            return 0

        print(f"💾 Loading {len(properties)} properties to database...")

        loaded_count = 0

        db = next(get_db())

        try:
            for prop_data in properties:
                formatted_address = prop_data.get("formattedAddress")
                if formatted_address:
                    existing = db.query(Property).filter(
                        Property.formatted_address == formatted_address
                    ).first()

                    if existing:
                        print(f"⚠️ Property already exists: {formatted_address}")
                        continue

                property_obj = self.create_property_from_api_data(prop_data, db)

                if property_obj:
                    try:
                        db.add(property_obj)
                        db.commit()
                        loaded_count += 1
                        print(f"✅ Loaded property {loaded_count}: {formatted_address}")

                    except Exception as e:
                        print(f"❌ Database error for {formatted_address}: {str(e)}")
                        db.rollback()
                        continue
                else:
                    print(f"❌ Failed to create property object")

        except Exception as e:
            print(f"❌ Critical error during loading: {str(e)}")
            db.rollback()
        finally:
            db.close()

        print(f"🎉 Successfully loaded {loaded_count} properties!")
        return loaded_count

    def run(self, mode: str = "random", count: int = 100):
        print("🚀 Starting RentCast property loader...")
        print(f"📊 Mode: {mode}, Count: {count}")

        if mode == "random":
            properties = self.fetch_random_properties(count)

            if properties:
                print(f"✅ Fetched {len(properties)} properties from API")
                loaded = self.load_properties_to_database(properties)
                print(f"🎯 Final result: {loaded} properties loaded successfully")
            else:
                print("❌ No properties fetched from API")
        else:
            print(f"❌ Unknown mode: {mode}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python load_properties_from_rentcast.py <mode> <count>")
        print("Example: python load_properties_from_rentcast.py random 100")
        sys.exit(1)

    mode = sys.argv[1]
    try:
        count = int(sys.argv[2])
        if count <= 0 or count > 500:
            raise ValueError("Count must be between 1 and 500")
    except ValueError:
        print("❌ Count must be a valid number between 1 and 500")
        sys.exit(1)

    if not settings.RENTCAST_API_KEY:
        print("❌ RENTCAST_API_KEY not found in environment variables")
        print("💡 Please set your RentCast API key in your .env file:")
        print("   RENTCAST_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        loader = RentCastPropertyLoader()
        loader.run(mode, count)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()