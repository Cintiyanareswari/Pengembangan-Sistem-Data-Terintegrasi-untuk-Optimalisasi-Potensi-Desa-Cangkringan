
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    BahanOrganik,
    Produk,
    Produksi,
    Penjualan,
    PrediksiPenjualan,
)


def get_dashboard_summary(db: Session):
    total_bahan_organik = (
        db.query(func.count(BahanOrganik.bahan_id)).scalar() or 0
    )

    total_produk = (
        db.query(func.count(Produk.produk_id)).scalar() or 0
    )

    total_produksi = (
        db.query(func.count(Produksi.produksi_id)).scalar() or 0
    )

    total_penjualan = (
        db.query(func.count(Penjualan.Penjualan_id)).scalar() or 0
    )

    total_prediksi = (
        db.query(func.count(PrediksiPenjualan.id)).scalar() or 0
    )

    total_prediksi_2026 = (
        db.query(
            func.sum(PrediksiPenjualan.prediksi_penjualan)
        )
        .filter(
            func.extract("year", PrediksiPenjualan.bulan) == 2026
        )
        .scalar()
        or 0
    )

    return {
        "total_bahan_organik": total_bahan_organik,
        "total_produk": total_produk,
        "total_data_produksi": total_produksi,
        "total_data_penjualan": total_penjualan,
        "total_data_prediksi": total_prediksi,
        "total_prediksi_penjualan_2026": float(total_prediksi_2026),
    }