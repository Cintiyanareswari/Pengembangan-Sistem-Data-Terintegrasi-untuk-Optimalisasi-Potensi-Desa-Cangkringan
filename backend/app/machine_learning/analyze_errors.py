
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("storage/machine_learning")

INPUT_PATH = DATA_DIR / "hasil_evaluasi_onehot.csv"
OUTPUT_PATH = DATA_DIR / "analisis_error_per_produk.csv"


def main():
    print("=" * 55)
    print("ANALISIS KESALAHAN PREDIKSI PER PRODUK VINIX7")
    print("=" * 55)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    hasil = df.groupby("Produk").apply(
        lambda data: pd.Series({
            "Total_Aktual": data["Aktual"].sum(),
            "Total_Prediksi": data["Prediksi"].sum(),
            "MAE": np.abs(
                data["Aktual"] - data["Prediksi"]
            ).mean(),
            "RMSE": np.sqrt(
                np.mean(
                    (data["Aktual"] - data["Prediksi"]) ** 2
                )
            ),
            "WAPE": (
                np.abs(
                    data["Aktual"] - data["Prediksi"]
                ).sum()
                / np.abs(data["Aktual"]).sum() * 100
                if np.abs(data["Aktual"]).sum() != 0
                else np.nan
            )
        }),
        include_groups=False
    ).reset_index()

    hasil = hasil.sort_values(
        "WAPE",
        ascending=False,
        na_position="last"
    )

    print("\nHASIL ANALISIS PER PRODUK")
    print("-" * 55)
    print(hasil.round(3).to_string(index=False))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hasil.to_csv(OUTPUT_PATH, index=False)

    print("\nFile tersimpan di:", OUTPUT_PATH)
    print("\nANALISIS ERROR SELESAI!")


if __name__ == "__main__":
    main()
