
from pydantic import BaseModel, ConfigDict


class RankingOrganikBase(BaseModel):
    peringkat: int
    jenis_bahan_organik: str
    skor_akhir: float


class RankingOrganikResponse(RankingOrganikBase):
    model_config = ConfigDict(from_attributes=True)