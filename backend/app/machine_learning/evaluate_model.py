
import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_DIR = Path("storage/machine_learning")
MODEL_PATH = Path("backend/models/extra_trees_model.pkl")
TEST_PATH = DATA_DIR / "data_test.csv"
OUTPUT_PATH = DATA_DIR / "hasil_evaluasi_onehot.csv"

FITUR = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_12",
    "bulan",
    "tahun",
    "bulan_sin",
    "bulan_cos",
    "Produk",
]

TARGET = "Jumlah_Terjual"


def main():
    print("=" * 50)
    print("EVALUASI MODEL EXTRA TREES + ONE-HOT ENCODING")
    print("=" * 50)

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan: {MODEL_PATH}"
        )

    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Data testing tidak ditemukan: {TEST_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(TEST_PATH)

    X_test = df[FITUR].copy()
    y_test = pd.to_numeric(df[TARGET], errors="coerce")

    data_valid = X_test.notna().all(axis=1) & y_test.notna()
    X_test = X_test.loc[data_valid]
    y_test = y_test.loc[data_valid]
    data_uji = df.loc[data_valid].copy()

    print("\nJumlah data testing:", len(X_test))
    print("Jumlah produk:", data_uji["Produk"].nunique())
    print("Memulai evaluasi model...")

    prediksi = model.predict(X_test)

    mae = mean_absolute_error(y_test, prediksi)
    rmse = np.sqrt(mean_squared_error(y_test, prediksi))

    total_aktual = np.abs(y_test).sum()

    if total_aktual != 0:
        wape = (
            np.abs(y_test - prediksi).sum()
            / total_aktual
        ) * 100
    else:
        wape = np.nan

    hasil = data_uji[["Bulan", "Produk"]].copy()
    hasil["Aktual"] = y_test.values
    hasil["Prediksi"] = prediksi
    hasil["Error_Absolut"] = np.abs(
        y_test.values - prediksi
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hasil.to_csv(OUTPUT_PATH, index=False)

    print("\nHASIL EVALUASI MODEL")
    print("-" * 50)
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"WAPE : {wape:.2f}%")

    print("\nFile hasil evaluasi tersimpan di:")
    print(OUTPUT_PATH)

    print("\nEVALUASI MODEL SELESAI!")


if __name__ == "__main__":
    main()
