
from sqlalchemy import inspect, text

from database.connection import engine


def test_database():

    print("\n=== PENGUJIAN DATABASE VINIX7 ===")

    # 1. Menguji koneksi PostgreSQL
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1

    print("Koneksi PostgreSQL: BERHASIL")

    # 2. Memeriksa tabel database
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    tabel_wajib = [
        "produk",
        "produksi",
        "penjualan",
        "prediksi_penjualan",
        "hasil_analisis_organik",
        "bobot_ahp",
        "hasil_scoring_organik",
        "ranking_organik",
    ]

    for tabel in tabel_wajib:
        assert tabel in tables, f"Tabel {tabel} tidak ditemukan"

    print("Pemeriksaan tabel: BERHASIL")

    # 3. Memeriksa jumlah data utama
    with engine.connect() as connection:

        jumlah_produk = connection.execute(
            text("SELECT COUNT(*) FROM produk")
        ).scalar()

        jumlah_produksi = connection.execute(
            text("SELECT COUNT(*) FROM produksi")
        ).scalar()

        jumlah_penjualan = connection.execute(
            text("SELECT COUNT(*) FROM penjualan")
        ).scalar()

        jumlah_prediksi = connection.execute(
            text("SELECT COUNT(*) FROM prediksi_penjualan")
        ).scalar()

    assert jumlah_produk == 11
    assert jumlah_produksi == 66
    assert jumlah_penjualan == 792
    assert jumlah_prediksi == 132

    print("Pemeriksaan jumlah data: BERHASIL")

    print("\nSEMUA PENGUJIAN DATABASE BERHASIL!")


if __name__ == "__main__":
    test_database()
