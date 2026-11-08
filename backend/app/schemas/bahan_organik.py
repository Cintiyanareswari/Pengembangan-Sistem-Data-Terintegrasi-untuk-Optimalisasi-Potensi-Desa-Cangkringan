
from pydantic import BaseModel, ConfigDict
from typing import Optional


class BahanOrganikBase(BaseModel):
    jenis_bahan_organik: str
    kategori_bahan: Optional[str] = None


class BahanOrganikCreate(BahanOrganikBase):
    bahan_id: str


class BahanOrganikResponse(BahanOrganikBase):
    bahan_id: str

    model_config = ConfigDict(from_attributes=True)