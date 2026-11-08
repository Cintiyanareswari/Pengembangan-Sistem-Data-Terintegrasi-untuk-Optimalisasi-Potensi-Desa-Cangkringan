
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.routes.dashboard import dashboard_summary


def test_dashboard_route():
    with Session(engine) as db:
        hasil = dashboard_summary(db)

        print("\n=== HASIL DASHBOARD ROUTE ===")

        for nama, nilai in hasil.items():
            print(f"{nama}: {nilai}")

        # Memastikan seluruh indikator tersedia
        assert "total_bahan_organik" in hasil
        assert "total_produk" in hasil
        assert "total_data_produksi" in hasil
        assert "total_data_penjualan" in hasil
        assert "total_data_prediksi" in hasil
        assert "total_prediksi_penjualan_2026" in hasil

        # Memastikan jumlah data sesuai database
        assert hasil["total_bahan_organik"] == 17
        assert hasil["total_produk"] == 11
        assert hasil["total_data_produksi"] == 66
        assert hasil["total_data_penjualan"] == 792
        assert hasil["total_data_prediksi"] == 132

        print("\nPengujian dashboard route berhasil!")


if __name__ == "__main__":
    test_dashboard_route()
