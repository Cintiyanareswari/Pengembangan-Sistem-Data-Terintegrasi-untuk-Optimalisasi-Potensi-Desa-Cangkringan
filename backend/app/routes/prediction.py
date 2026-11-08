
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db

from backend.app.services.prediction_service import (
    get_prediction_2026,
    get_prediction_summary
)

from backend.app.schemas.prediksi_penjualan import (
    PrediksiPenjualanResponse
)


router = APIRouter(
    prefix="/prediction",
    tags=["Prediksi Penjualan"]
)


@router.get(
    "/2026",
    response_model=list[PrediksiPenjualanResponse]
)
def prediction_2026(db: Session = Depends(get_db)):
    return get_prediction_2026(db)


@router.get("/summary")
def prediction_summary(db: Session = Depends(get_db)):
    return get_prediction_summary(db)
