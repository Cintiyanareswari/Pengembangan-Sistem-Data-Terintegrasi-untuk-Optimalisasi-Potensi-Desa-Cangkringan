
from pathlib import Path
import joblib
import pandas as pd

# Lokasi file proyek
ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT_DIR / "backend" / "models" / "extra_trees_final_2026.pkl"
PREDICTION_PATH = (
    ROOT_DIR / "storage" / "machine_learning" / "hasil_prediksi_2026.csv"
)


def test_machine_learning():

    print("\n=== PENGUJIAN MACHINE LEARNING VINIX7 ===")

    # 1. Memeriksa file model
    assert MODEL_PATH.exists(), "File model tidak ditemukan"

    model = joblib.load(MODEL_PATH)
    assert model is not None

    print("Pemeriksaan model: BERHASIL")

    # 2. Memeriksa hasil prediksi
    assert PREDICTION_PATH.exists(), "File prediksi tidak ditemukan"

    df = pd.read_csv(PREDICTION_PATH)

    assert len(df) == 132, "Jumlah prediksi tidak sesuai"
    assert df["Produk"].nunique() == 11, "Jumlah produk tidak sesuai"
    assert df["Prediksi_Penjualan"].notna().all()

    print("Pemeriksaan hasil prediksi: BERHASIL")

    # 3. Memeriksa periode prediksi
    df["Bulan"] = pd.to_datetime(df["Bulan"])

    assert df["Bulan"].dt.year.eq(2026).all()
    assert df["Bulan"].nunique() == 12

    print("Pemeriksaan periode prediksi: BERHASIL")

    print("\nSEMUA PENGUJIAN MACHINE LEARNING BERHASIL!")


if __name__ == "__main__":
    test_machine_learning()
