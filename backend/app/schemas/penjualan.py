
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PenjualanBase(BaseModel):
    Produk_id: str

    bulan: Optional[date] = None
    nama_produk: Optional[str] = None
    jumlah_terjual: Optional[int] = None

    harga_satuan: Optional[Decimal] = None
    total_penjualan: Optional[Decimal] = None

    satuan: Optional[str] = None
    kanal: Optional[str] = None
    status_data: Optional[str] = None


class PenjualanCreate(PenjualanBase):
    Penjualan_id: str


class PenjualanResponse(PenjualanBase):
    Penjualan_id: str

    model_config = ConfigDict(from_attributes=True)