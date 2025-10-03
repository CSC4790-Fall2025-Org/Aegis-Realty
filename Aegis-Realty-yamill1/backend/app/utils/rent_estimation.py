import math
from typing import List, Dict, Any, Optional


class RentEstimator:

    def calculate_weighted_rent_estimate(self, comparables: List[Dict[str, Any]],
                                         subject_property: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate rent estimate using weighted average based on distance and similarity
        (mimics RentCast's methodology)
        """
        if not comparables:
            return {"rent": 0, "rentRangeLow": 0, "rentRangeHigh": 0}

        weighted_rents = []
        total_weight = 0

        for comp in comparables:
            # Calculate weight based on correlation (if available) and distance
            correlation = comp.get("correlation", 0.5)  # Default correlation
            distance = comp.get("distance", 1.0)  # Default distance in miles

            # Weight calculation: higher correlation and lower distance = higher weight
            # Inverse distance weighting with correlation boost
            weight = correlation / max(distance, 0.1)  # Prevent division by zero

            rent = comp.get("price", 0)
            if rent > 0:
                weighted_rents.append(rent * weight)
                total_weight += weight

        if total_weight == 0:
            return {"rent": 0, "rentRangeLow": 0, "rentRangeHigh": 0}

        # Calculate weighted average
        estimated_rent = sum(weighted_rents) / total_weight

        # Calculate range (±5-10% based on data quality)
        range_factor = 0.075  # 7.5% range
        rent_low = estimated_rent * (1 - range_factor)
        rent_high = estimated_rent * (1 + range_factor)

        return {
            "rent": round(estimated_rent),
            "rentRangeLow": round(rent_low),
            "rentRangeHigh": round(rent_high)
        }

    def find_similar_properties(self, properties: List[Dict[str, Any]],
                                subject_property: Dict[str, Any],
                                max_distance_miles: float = 5.0) -> List[Dict[str, Any]]:
        """
        Find similar properties for rent estimation (backup method)
        """
        subject_lat = subject_property.get("latitude")
        subject_lon = subject_property.get("longitude")
        subject_beds = subject_property.get("bedrooms", 0)
        subject_baths = subject_property.get("bathrooms", 0)
        subject_sqft = subject_property.get("squareFootage", 0)

        if not all([subject_lat, subject_lon]):
            return []

        similar_props = []

        for prop in properties:
            # Skip if missing essential data
            if not all([prop.get("latitude"), prop.get("longitude"), prop.get("lastSalePrice")]):
                continue

            # Calculate distance
            distance = self._calculate_distance(
                subject_lat, subject_lon,
                prop.get("latitude"), prop.get("longitude")
            )

            if distance > max_distance_miles:
                continue

            # Calculate similarity score
            similarity = self._calculate_similarity(subject_property, prop)

            similar_props.append({
                **prop,
                "distance": distance,
                "correlation": similarity,
                "price": self._estimate_rent_from_sale_price(prop.get("lastSalePrice", 0))
            })

        # Sort by correlation and distance, return top 5
        similar_props.sort(key=lambda x: (x["correlation"], -x["distance"]), reverse=True)
        return similar_props[:5]

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 3959  # Earth's radius in miles

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def _calculate_similarity(self, subject: Dict[str, Any], comp: Dict[str, Any]) -> float:
        """Calculate similarity score between properties"""
        score = 0.0
        total_weight = 0.0

        # Bedroom similarity (weight: 0.3)
        if subject.get("bedrooms") and comp.get("bedrooms"):
            bed_diff = abs(subject["bedrooms"] - comp["bedrooms"])
            bed_score = max(0, 1 - (bed_diff * 0.2))  # Penalty for each bedroom difference
            score += bed_score * 0.3
            total_weight += 0.3

        # Bathroom similarity (weight: 0.2)
        if subject.get("bathrooms") and comp.get("bathrooms"):
            bath_diff = abs(subject["bathrooms"] - comp["bathrooms"])
            bath_score = max(0, 1 - (bath_diff * 0.3))
            score += bath_score * 0.2
            total_weight += 0.2

        # Square footage similarity (weight: 0.3)
        if subject.get("squareFootage") and comp.get("squareFootage"):
            sqft_diff = abs(subject["squareFootage"] - comp["squareFootage"])
            sqft_ratio = sqft_diff / max(subject["squareFootage"], 1)
            sqft_score = max(0, 1 - sqft_ratio)
            score += sqft_score * 0.3
            total_weight += 0.3

        # Property type similarity (weight: 0.2)
        if subject.get("propertyType") and comp.get("propertyType"):
            type_score = 1.0 if subject["propertyType"] == comp["propertyType"] else 0.5
            score += type_score * 0.2
            total_weight += 0.2

        return score / total_weight if total_weight > 0 else 0.5

    def _estimate_rent_from_sale_price(self, sale_price: float) -> float:
        """Rough estimate: rent is typically 0.8-1.2% of property value per month"""
        if sale_price <= 0:
            return 0
        return sale_price * 0.01  # 1% rule as rough estimate
