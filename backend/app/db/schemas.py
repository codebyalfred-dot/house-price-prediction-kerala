from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.data.city_profiles import SUPPORTED_LOCATIONS


FurnishingType = Literal["None", "Semi", "Full"]
FacingType = Literal["East", "West", "North", "South"]
PropertyType = Literal["Apartment", "Villa"]


class PredictionRequest(BaseModel):
    location: str = Field(..., description="Selected Kerala city.")
    bhk: int = Field(..., ge=1, le=10)
    area_sqft: float = Field(..., gt=200, le=12000)
    bathrooms: int = Field(..., ge=1, le=10)
    age_of_property: int = Field(..., ge=0, le=80)
    floor: int = Field(..., ge=0, le=80)
    total_floors: int = Field(..., ge=1, le=100)
    parking: bool
    furnishing: FurnishingType
    facing: FacingType
    property_type: PropertyType

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        if value not in SUPPORTED_LOCATIONS:
            raise ValueError(f"Unsupported location. Choose from: {', '.join(SUPPORTED_LOCATIONS)}")
        return value

    @model_validator(mode="after")
    def validate_floor_logic(self) -> "PredictionRequest":
        if self.floor > self.total_floors:
            raise ValueError("Floor cannot be greater than total floors.")
        return self


class PredictionResponse(BaseModel):
    predicted_price_lakhs: float
    predicted_price_inr: float
    formatted_price: str
    investment_score: str
    investment_score_value: int
    area_popularity: str
    city_average_price_lakhs: float
    delta_from_city_average_lakhs: float
    price_position: str
    confidence_band_lakhs: dict[str, float]
    summary: str
    model_loaded: bool


class WeatherInfo(BaseModel):
    temperature_c: float
    condition: str
    humidity: int
    wind_speed_kph: float
    source: str


class NearbyFacility(BaseModel):
    name: str
    category: str
    distance_km: float
    address: str


class Coordinates(BaseModel):
    lat: float
    lng: float


class LocationInfoResponse(BaseModel):
    location: str
    coordinates: Coordinates
    map_embed_url: str
    weather: WeatherInfo
    nearby_facilities: list[NearbyFacility]
    climate_summary: str
    area_highlights: list[str]
    hero_image_url: str


class PortalRecommendation(BaseModel):
    name: str
    url: str
    note: str


class RecommendationResponse(BaseModel):
    location: str
    property_type: PropertyType
    budget_lakhs: float | None = None
    portals: list[PortalRecommendation]
    local_tips: list[str]
    suggested_localities: list[str]


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    is_active: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
