from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Kerala House Price Prediction System"
    debug: bool = True
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = f"sqlite:///{(BASE_DIR / 'kerala_house_price.db').as_posix()}"
    allowed_origins: str = (
        "http://localhost:5173,http://localhost:4173,http://localhost:3000,"
        "http://127.0.0.1:5173,http://127.0.0.1:4173,http://127.0.0.1:3000"
    )
    google_maps_api_key: str | None = None
    openweather_api_key: str | None = None
    unsplash_access_key: str | None = None
    model_path: str = "models/house_price_model.joblib"
    metadata_path: str = "models/model_metadata.json"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def resolved_model_path(self) -> Path:
        return BASE_DIR / self.model_path

    @property
    def resolved_metadata_path(self) -> Path:
        return BASE_DIR / self.metadata_path


@lru_cache
def get_settings() -> Settings:
    return Settings()
