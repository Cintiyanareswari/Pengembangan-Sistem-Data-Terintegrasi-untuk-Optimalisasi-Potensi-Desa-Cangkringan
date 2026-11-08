
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import PrediksiPenjualan


def get_prediction_2026(db: Session):
    """
    Mengambil seluruh data prediksi penjualan tahun 2026.
    """

    data = (
        db.query(PrediksiPenjualan)
        .filter(
            func.extract("year", PrediksiPenjualan.bulan) == 2026
        )
        .order_by(
            PrediksiPenjualan.bulan.asc(),
            PrediksiPenjualan.produk.asc()
        )
        .all()
    )

    return data


def get_prediction_summary(db: Session):
    """
    Menghitung total prediksi penjualan per produk tahun 2026.
    """

    data = (
        db.query(
            PrediksiPenjualan.produk,
            func.sum(
                PrediksiPenjualan.prediksi_penjualan
            ).label("total_prediksi")
        )
        .filter(
            func.extract("year", PrediksiPenjualan.bulan) == 2026
        )
        .group_by(PrediksiPenjualan.produk)
        .order_by(
            func.sum(
                PrediksiPenjualan.prediksi_penjualan
            ).desc()
        )
        .all()
    )

    return [
        {
            "produk": row.produk,
            "total_prediksi": float(row.total_prediksi or 0)
        }
        for row in data
    ]