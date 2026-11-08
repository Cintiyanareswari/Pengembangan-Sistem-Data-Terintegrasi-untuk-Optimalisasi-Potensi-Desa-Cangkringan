
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

STORAGE_DIR = ROOT_DIR / "storage" / "analysis"


def test_analysis():

    print("\n=== PENGUJIAN ANALISIS VINIX7 ===")

    # 1. Memeriksa hasil EDA produksi
    file_produksi = STORAGE_DIR / "hasil_eda_produksi.csv"
    assert file_produksi.exists(), "File EDA produksi tidak ditemukan"

    df_produksi = pd.read_csv(file_produksi)
    assert not df_produksi.empty

    print("EDA produksi: BERHASIL")

    # 2. Memeriksa hasil EDA penjualan
    file_penjualan = STORAGE_DIR / "hasil_eda_penjualan.csv"
    assert file_penjualan.exists(), "File EDA penjualan tidak ditemukan"

    df_penjualan = pd.read_csv(file_penjualan)
    assert not df_penjualan.empty

    print("EDA penjualan: BERHASIL")

    # 3. Memeriksa analisis bahan organik
    file_organik = STORAGE_DIR / "analisis_organik.csv"
    assert file_organik.exists(), "File analisis organik tidak ditemukan"

    df_organik = pd.read_csv(file_organik)
    assert len(df_organik) == 88

    print("Analisis bahan organik: BERHASIL")

    # 4. Memeriksa hasil ranking organik
    file_ranking = STORAGE_DIR / "ranking_organik.csv"
    assert file_ranking.exists(), "File ranking organik tidak ditemukan"

    df_ranking = pd.read_csv(file_ranking)
    assert len(df_ranking) == 17

    print("Ranking bahan organik: BERHASIL")

    print("\nSEMUA PENGUJIAN ANALISIS BERHASIL!")


if __name__ == "__main__":
    test_analysis()
