
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProdukBase(BaseModel):
    nama_produk: str
    jenis_produk: Optional[str] = None
    deskripsi: Optional[str] = None
    manfaat: Optional[str] = None
    harga: Optional[Decimal] = None
    ukuran_kemasan: Optional[str] = None
    produsen: Optional[str] = None
    lokasi_produsen: Optional[str] = None
    kontak: Optional[str] = None
    stok_ketersediaan: Optional[str] = None
    foto_produk: Optional[str] = None


class ProdukCreate(ProdukBase):
    produk_id: str


class ProdukResponse(ProdukBase):
    produk_id: str

    model_config = ConfigDict(from_attributes=True)