
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class KetersediaanBahanBase(BaseModel):
    bahan_id: str
    padukuhan_id: str
    periode: Optional[date] = None

    jumlah_ketersediaan: Optional[float] = None
    satuan: Optional[str] = None

    kontinuitas: Optional[str] = None
    jarak_ke_produksi_km: Optional[float] = None

    kemudahan_pengumpulan: Optional[str] = None
    status_pemanfaatan: Optional[str] = None

    frekuensi: Optional[str] = None
    musim: Optional[str] = None

    jumlah_sumber: Optional[int] = None
    status_data: Optional[str] = None


class KetersediaanBahanCreate(KetersediaanBahanBase):
    ketersediaan_id: str


class KetersediaanBahanResponse(KetersediaanBahanBase):
    ketersediaan_id: str

    model_config = ConfigDict(from_attributes=True)