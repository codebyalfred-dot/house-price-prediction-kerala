import logging
from pathlib import Path

import joblib
import pandas as pd

from app.core.config import get_settings
from app.data.city_profiles import CITY_PROFILES
from app.db.schemas import PredictionRequest


logger = logging.getLogger(__name__)


class KeralaHousePricePredictor:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = None
        self.model_loaded = False
        self._load_model()

    def _load_model(self) -> None:
        model_path = Path(self.settings.resolved_model_path)
        if model_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.model_loaded = True
            except Exception as exc:
                logger.warning("Unable to load trained model, using heuristic fallback: %s", exc)

    def predict(self, payload: PredictionRequest) -> float:
        features = self._build_feature_frame(payload)
        if self.model_loaded and self.model is not None:
            prediction = float(self.model.predict(features)[0])
            return round(max(prediction, 10.0), 2)
        return round(self._fallback_predict(payload), 2)

    def confidence_band(self, predicted_price_lakhs: float) -> dict[str, float]:
        margin = predicted_price_lakhs * 0.08
        return {
            "lower": round(max(predicted_price_lakhs - margin, 0), 2),
            "upper": round(predicted_price_lakhs + margin, 2),
        }

    def _build_feature_frame(self, payload: PredictionRequest) -> pd.DataFrame:
        city_profile = CITY_PROFILES[payload.location]
        row = {
            "location": payload.location,
            "bhk": payload.bhk,
            "area_sqft": payload.area_sqft,
            "bathrooms": payload.bathrooms,
            "age_of_property": payload.age_of_property,
            "floor": payload.floor,
            "total_floors": payload.total_floors,
            "parking": int(payload.parking),
            "furnishing": payload.furnishing,
            "facing": payload.facing,
            "property_type": payload.property_type,
            "city_avg_price_per_sqft": city_profile["average_price_per_sqft"],
            "floor_ratio": round(payload.floor / max(payload.total_floors, 1), 3),
        }
        return pd.DataFrame([row])

    def _fallback_predict(self, payload: PredictionRequest) -> float:
        profile = CITY_PROFILES[payload.location]
        base_price = profile["average_price_per_sqft"] * payload.area_sqft / 100000
        property_multiplier = 1.12 if payload.property_type == "Villa" else 1.0
        age_factor = max(0.72, 1 - (payload.age_of_property * 0.008))
        furnishing_factor = {"None": 0.96, "Semi": 1.02, "Full": 1.08}[payload.furnishing]
        facing_factor = {"East": 1.01, "West": 0.99, "North": 1.0, "South": 1.02}[payload.facing]
        parking_factor = 1.03 if payload.parking else 0.98
        bhk_adjustment = payload.bhk * 1.6
        bathroom_adjustment = payload.bathrooms * 1.1
        floor_premium = 1.0
        if payload.property_type == "Apartment":
            floor_premium += min(payload.floor, 12) * 0.005

        prediction = (
            base_price * property_multiplier * age_factor * furnishing_factor * facing_factor * parking_factor * floor_premium
        ) + bhk_adjustment + bathroom_adjustment
        return prediction


predictor = KeralaHousePricePredictor()
