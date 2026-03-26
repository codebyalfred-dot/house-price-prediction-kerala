from fastapi import APIRouter

from app.ml.predictor import predictor


router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "model_loaded": predictor.model_loaded,
        "message": "API is healthy and ready to serve predictions.",
    }

