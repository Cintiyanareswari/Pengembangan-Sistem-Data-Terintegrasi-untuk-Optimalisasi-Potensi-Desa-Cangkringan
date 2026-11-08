
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnalisisOrganikBase(BaseModel):
    bahan_id: str
    jenis_bahan_organik: str
    kategori_bahan: Optional[str] = None

    jumlah_ketersediaan: Optional[float] = None
    satuan: Optional[str] = None
    kontinuitas: Optional[str] = None

    jarak_ke_produksi_km: Optional[float] = None
    kemudahan_pengumpulan: Optional[str] = None


class AnalisisOrganikResponse(AnalisisOrganikBase):
    model_config = ConfigDict(from_attributes=True)