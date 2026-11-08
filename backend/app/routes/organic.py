
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db

from backend.app.services.organic_service import (
    get_analisis_organik,
    get_ranking_organik
)

from backend.app.schemas.analisis_organik import AnalisisOrganikResponse
from backend.app.schemas.ranking_organik import RankingOrganikResponse


router = APIRouter(
    prefix="/organic",
    tags=["Analisis Bahan Organik"]
)


@router.get(
    "/analysis",
    response_model=list[AnalisisOrganikResponse]
)
def organic_analysis(db: Session = Depends(get_db)):
    return get_analisis_organik(db)


@router.get(
    "/ranking",
    response_model=list[RankingOrganikResponse]
)
def organic_ranking(db: Session = Depends(get_db)):
    return get_ranking_organik(db)
