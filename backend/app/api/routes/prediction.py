from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.data.city_profiles import SUPPORTED_LOCATIONS
from app.db.models import PredictionLog, User
from app.db.schemas import LocationInfoResponse, PredictionRequest, PredictionResponse, RecommendationResponse
from app.ml.predictor import predictor
from app.services.insight_service import InsightService
from app.services.location_service import location_service
from app.services.recommendation_service import recommendation_service


router = APIRouter(tags=["Prediction"])


@router.get("/cities")
def list_supported_cities() -> dict:
    return {"cities": SUPPORTED_LOCATIONS}


@router.post("/predict", response_model=PredictionResponse)
def predict_house_price(
    payload: PredictionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> PredictionResponse:
    predicted_price_lakhs = predictor.predict(payload)
    city_average_lakhs = InsightService.calculate_city_average_price_lakhs(
        payload.location,
        payload.area_sqft,
        payload.property_type,
    )
    investment_score_value, investment_score_label = InsightService.calculate_investment_score(
        payload,
        predicted_price_lakhs,
    )
    area_popularity = InsightService.area_popularity(payload.location, payload.property_type)
    delta = round(predicted_price_lakhs - city_average_lakhs, 2)
    confidence_band = predictor.confidence_band(predicted_price_lakhs)
    user_id = _resolve_user_id(request, db)

    db.add(
        PredictionLog(
            user_id=user_id,
            location=payload.location,
            property_type=payload.property_type,
            bhk=payload.bhk,
            area_sqft=payload.area_sqft,
            predicted_price_lakhs=predicted_price_lakhs,
            investment_score=investment_score_label,
        )
    )
    db.commit()

    return PredictionResponse(
        predicted_price_lakhs=predicted_price_lakhs,
        predicted_price_inr=round(predicted_price_lakhs * 100000, 2),
        formatted_price=_format_price(predicted_price_lakhs),
        investment_score=investment_score_label,
        investment_score_value=investment_score_value,
        area_popularity=area_popularity,
        city_average_price_lakhs=city_average_lakhs,
        delta_from_city_average_lakhs=delta,
        price_position=InsightService.classify_price_position(predicted_price_lakhs, city_average_lakhs),
        confidence_band_lakhs=confidence_band,
        summary=InsightService.build_summary(
            payload.location,
            predicted_price_lakhs,
            city_average_lakhs,
            investment_score_label,
        ),
        model_loaded=predictor.model_loaded,
    )


@router.get("/location-info", response_model=LocationInfoResponse)
async def get_location_info(
    location: str = Query(..., description="Kerala city to inspect."),
    property_type: str = Query("Apartment"),
) -> LocationInfoResponse:
    if location not in SUPPORTED_LOCATIONS:
        raise HTTPException(status_code=400, detail="Unsupported location.")

    return LocationInfoResponse.model_validate(
        await location_service.get_location_info(location, property_type)
    )


@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    location: str = Query(..., description="Kerala city to inspect."),
    property_type: str = Query("Apartment"),
    budget_lakhs: float | None = Query(default=None),
) -> RecommendationResponse:
    if location not in SUPPORTED_LOCATIONS:
        raise HTTPException(status_code=400, detail="Unsupported location.")

    return RecommendationResponse.model_validate(
        recommendation_service.get_recommendations(location, property_type, budget_lakhs)
    )


def _format_price(price_lakhs: float) -> str:
    if price_lakhs >= 100:
        return f"INR {price_lakhs / 100:.2f} Cr"
    return f"INR {price_lakhs:.2f} Lakhs"


def _resolve_user_id(request: Request, db: Session) -> int | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "", 1).strip()
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        return None

    user = db.get(User, user_id)
    return user.id if user else None
