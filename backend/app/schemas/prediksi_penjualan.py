
from datetime import date
from pydantic import BaseModel, ConfigDict


class PrediksiPenjualanBase(BaseModel):
    bulan: date
    produk: str
    prediksi_penjualan: float
    model: str
    tanggal_prediksi: date


class PrediksiPenjualanCreate(PrediksiPenjualanBase):
    pass


class PrediksiPenjualanResponse(PrediksiPenjualanBase):
    id: int

    model_config = ConfigDict(from_attributes=True)