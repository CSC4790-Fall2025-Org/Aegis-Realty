import sys
import os
import requests
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.property import Property
from app.core.config import settings


class RentCastPropertyLoader:
    def __init__(self):
        self.api_key = settings.RENTCAST_API_KEY
        self.headers = {"X-Api-Key": self.api_key}
        self.base_url = "https://api.rentcast.io/v1"

    def load_random_properties(self, limit: int = 500):
        """Load random properties from RentCast"""

        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        try:
            print(f"🔍 Fetching {limit} random properties from RentCast...")

            url = f"{self.base_url}/properties/random"
            params = {"limit": limit}

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            properties_data = response.json()

            if not properties_data:
                print("❌ No properties returned from API")
                return

            print(f"📦 Received {len(properties_data)} properties from API")

            loaded_count = 0
            skipped_count = 0

            for prop_data in properties_data:
                try:
                    # Extract address
                    address = prop_data.get("formattedAddress") or prop_data.get("addressLine1", "")
                    if not address:
                        skipped_count += 1
                        continue

                    # Check if property already exists
                    existing = db.query(Property).filter(Property.address == address).first()
                    if existing:
                        skipped_count += 1
                        continue

                    # Create property record
                    property_obj = Property(
                        address=address,
                        city=prop_data.get("city", ""),
                        state=prop_data.get("state", ""),
                        zip_code=prop_data.get("zipCode", ""),
                        price=prop_data.get("lastSalePrice", 0.0),
                        bedrooms=prop_data.get("bedrooms", 0),
                        bathrooms=prop_data.get("bathrooms", 0.0),
                        square_feet=prop_data.get("squareFootage", 0),
                        year_built=prop_data.get("yearBuilt", None)
                    )

                    db.add(property_obj)
                    loaded_count += 1

                    if loaded_count % 50 == 0:
                        print(f"✅ Processed {loaded_count} properties...")

                except Exception as e:
                    print(f"❌ Error processing property: {str(e)}")
                    skipped_count += 1
                    continue

            # Commit all at once
            db.commit()

            print(f"\n🎉 Successfully loaded {loaded_count} properties!")
            if skipped_count > 0:
                print(f"⏭️  Skipped {skipped_count} properties (duplicates or missing data)")

        except requests.exceptions.RequestException as e:
            print(f"❌ RentCast API error: {str(e)}")
            db.rollback()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def load_properties_by_location(self, city: str = None, state: str = None,
                                    zip_code: str = None, limit: int = 500, offset: int = 0):
        """Load properties by location with pagination"""

        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        try:
            print(f"🔍 Fetching properties for {city or ''} {state or ''} {zip_code or ''}...")

            url = f"{self.base_url}/properties"
            params = {
                "limit": limit,
                "offset": offset
            }

            if city:
                params["city"] = city
            if state:
                params["state"] = state
            if zip_code:
                params["zipCode"] = zip_code

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            properties_data = response.json()

            if not properties_data:
                print("❌ No properties returned from API")
                return

            print(f"📦 Received {len(properties_data)} properties from API")

            loaded_count = 0
            skipped_count = 0

            for prop_data in properties_data:
                try:
                    address = prop_data.get("formattedAddress") or prop_data.get("addressLine1", "")
                    if not address:
                        skipped_count += 1
                        continue

                    existing = db.query(Property).filter(Property.address == address).first()
                    if existing:
                        skipped_count += 1
                        continue

                    property_obj = Property(
                        address=address,
                        city=prop_data.get("city", ""),
                        state=prop_data.get("state", ""),
                        zip_code=prop_data.get("zipCode", ""),
                        price=prop_data.get("lastSalePrice", 0.0),
                        bedrooms=prop_data.get("bedrooms", 0),
                        bathrooms=prop_data.get("bathrooms", 0.0),
                        square_feet=prop_data.get("squareFootage", 0),
                        year_built=prop_data.get("yearBuilt", None)
                    )

                    db.add(property_obj)
                    loaded_count += 1

                except Exception as e:
                    print(f"❌ Error processing property: {str(e)}")
                    skipped_count += 1
                    continue

            db.commit()

            print(f"\n🎉 Successfully loaded {loaded_count} properties!")
            if skipped_count > 0:
                print(f"⏭️  Skipped {skipped_count} properties")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.rollback()
        finally:
            db.close()


def show_current_count():
    """Show current property count in database"""
    db = SessionLocal()
    try:
        count = db.query(Property).count()
        print(f"📊 Current properties in database: {count}")
    finally:
        db.close()


if __name__ == "__main__":
    loader = RentCastPropertyLoader()

    print("🏠 RentCast Property Bulk Loader")
    print("=" * 40)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "random":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
            loader.load_random_properties(limit)

        elif command == "location":
            city = sys.argv[2] if len(sys.argv) > 2 else None
            state = sys.argv[3] if len(sys.argv) > 3 else None
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 500
            loader.load_properties_by_location(city, state, limit=limit)

        elif command == "count":
            show_current_count()

        else:
            print("❌ Unknown command")
    else:
        print("Usage:")
        print("  python3 load_properties_from_rentcast.py random [limit]")
        print("  python3 load_properties_from_rentcast.py location [city] [state] [limit]")
        print("  python3 load_properties_from_rentcast.py count")
        print()

        while True:
            print("\nOptions:")
            print("1. Load 500 random properties")
            print("2. Load properties by location")
            print("3. Show current count")
            print("4. Quit")

            choice = input("\nSelect option (1-4): ").strip()

            if choice == "1":
                try:
                    limit = int(input("How many properties? (default 500): ") or "500")
                    loader.load_random_properties(limit)
                    break
                except ValueError:
                    print("❌ Invalid number")

            elif choice == "2":
                city = input("City (optional): ").strip() or None
                state = input("State code (optional): ").strip().upper() or None
                try:
                    limit = int(input("How many properties? (default 500): ") or "500")
                    loader.load_properties_by_location(city, state, limit=limit)
                    break
                except ValueError:
                    print("❌ Invalid number")

            elif choice == "3":
                show_current_count()

            elif choice == "4":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice")