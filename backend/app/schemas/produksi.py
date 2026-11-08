
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProduksiBase(BaseModel):
    produk_id: str

    nama_produk: Optional[str] = None
    jenis_produk: Optional[str] = None

    jumlah_produksi_varian: Optional[int] = None
    jumlah_produksi_total: Optional[int] = None

    satuan: Optional[str] = None
    kapasitas_produk: Optional[int] = None

    bahan_baku_aktif: Optional[str] = None
    bahan_baku: Optional[str] = None
    jumlah_bahan_baku: Optional[str] = None

    periode_produksi: Optional[int] = None
    stok: Optional[str] = None
    status_data: Optional[str] = None

    satuan_bahan_baku: Optional[str] = None
    nilai_bahan_baku: Optional[int] = None

    satuan_stok: Optional[str] = None
    nilai_stok: Optional[int] = None


class ProduksiCreate(ProduksiBase):
    produksi_id: str


class ProduksiResponse(ProduksiBase):
    produksi_id: str

    model_config = ConfigDict(from_attributes=True)