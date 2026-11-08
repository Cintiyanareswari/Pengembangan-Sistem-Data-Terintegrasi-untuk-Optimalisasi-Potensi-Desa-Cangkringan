
from sqlalchemy.orm import Session

from database.connection import engine

from backend.app.routes.prediction import (
    prediction_2026,
    prediction_summary
)


def test_prediction_route():
    with Session(engine) as db:

        # 1. Menguji pengambilan prediksi tahun 2026
        hasil_prediksi = prediction_2026(db)

        print("\n=== HASIL PREDICTION 2026 ===")
        print(f"Total data prediksi: {len(hasil_prediksi)}")

        assert len(hasil_prediksi) == 132

        for data in hasil_prediksi[:5]:
            assert data.bulan is not None
            assert data.produk is not None
            assert data.prediksi_penjualan is not None

            print(
                f"{data.bulan} - {data.produk} - "
                f"{data.prediksi_penjualan}"
            )

        # 2. Menguji ringkasan prediksi per produk
        hasil_ringkasan = prediction_summary(db)

        print("\n=== RINGKASAN PREDIKSI PER PRODUK ===")
        print(f"Total produk: {len(hasil_ringkasan)}")

        assert len(hasil_ringkasan) == 11

        for data in hasil_ringkasan:
            assert data["produk"] is not None
            assert data["total_prediksi"] >= 0

            print(
                f"{data['produk']}: "
                f"{data['total_prediksi']:.2f}"
            )

        # 3. Menguji urutan prediksi terbesar
        print("\n=== PEMERIKSAAN PRODUK TERATAS ===")

        for data in hasil_ringkasan[:3]:
            print(
                f"{data['produk']}: "
                f"{data['total_prediksi']:.2f}"
            )

        assert (
            hasil_ringkasan[0]["produk"]
            == "Probiotik GB Proquatic"
        )

        assert (
            hasil_ringkasan[0]["total_prediksi"]
            >= hasil_ringkasan[1]["total_prediksi"]
        )

        assert (
            hasil_ringkasan[1]["total_prediksi"]
            >= hasil_ringkasan[2]["total_prediksi"]
        )

        print("\nPengujian prediction route berhasil!")


if __name__ == "__main__":
    test_prediction_route()
