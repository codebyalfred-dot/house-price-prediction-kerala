from app.data.city_profiles import CITY_PROFILES
from app.db.schemas import PredictionRequest


class InsightService:
    @staticmethod
    def calculate_city_average_price_lakhs(location: str, area_sqft: float, property_type: str) -> float:
        profile = CITY_PROFILES[location]
        type_factor = 1.1 if property_type == "Villa" else 1.0
        return round((profile["average_price_per_sqft"] * area_sqft * type_factor) / 100000, 2)

    @staticmethod
    def classify_price_position(predicted_price_lakhs: float, city_average_lakhs: float) -> str:
        delta_ratio = (predicted_price_lakhs - city_average_lakhs) / max(city_average_lakhs, 1)
        if delta_ratio <= -0.1:
            return "Below city average"
        if delta_ratio >= 0.1:
            return "Above city average"
        return "In line with city average"

    @staticmethod
    def calculate_investment_score(payload: PredictionRequest, predicted_price_lakhs: float) -> tuple[int, str]:
        profile = CITY_PROFILES[payload.location]
        city_average = InsightService.calculate_city_average_price_lakhs(
            payload.location,
            payload.area_sqft,
            payload.property_type,
        )
        ratio = predicted_price_lakhs / max(city_average, 1)

        score = 48
        score += 14 if profile["growth_rate"] >= 7.5 else 8 if profile["growth_rate"] >= 6 else 4
        score += 8 if payload.age_of_property <= 5 else 4 if payload.age_of_property <= 12 else -4
        score += 6 if payload.parking else 0
        score += 5 if payload.furnishing == "Full" else 2 if payload.furnishing == "Semi" else 0
        score += 4 if payload.property_type == "Villa" and payload.location in {"Wayanad", "Kottayam", "Kochi"} else 0
        score += 8 if ratio <= 0.96 else 2 if ratio <= 1.04 else -6

        score = max(0, min(100, score))
        label = "High" if score >= 72 else "Medium" if score >= 52 else "Low"
        return score, label

    @staticmethod
    def area_popularity(location: str, property_type: str) -> str:
        base = CITY_PROFILES[location]["popularity"]
        if property_type == "Villa" and location in {"Wayanad", "Kottayam"} and base == "Medium":
            return "Medium-High"
        return base

    @staticmethod
    def build_summary(
        location: str,
        predicted_price_lakhs: float,
        city_average_lakhs: float,
        investment_score_label: str,
    ) -> str:
        comparison = "below" if predicted_price_lakhs < city_average_lakhs else "above"
        return (
            f"The estimated value in {location} is INR {predicted_price_lakhs:.2f} lakhs, which is {comparison} "
            f"the local benchmark of INR {city_average_lakhs:.2f} lakhs. Based on price position, city momentum, "
            f"and property quality, this opportunity currently scores {investment_score_label.lower()} on investment potential."
        )
