
import pandas as pd
import joblib

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesRegressor


# ==========================================
# KONFIGURASI PATH
# ==========================================

DATA_DIR = Path("storage/machine_learning")
MODEL_DIR = Path("backend/models")

DATA_PATH = DATA_DIR / "dataset_model.csv"

MODEL_PATH = MODEL_DIR / "extra_trees_final_2026.pkl"


# ==========================================
# FITUR MODEL TERPILIH
# ==========================================

FITUR_NUMERIK = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_12",
    "bulan",
    "tahun",
    "bulan_sin",
    "bulan_cos",
]

FITUR_KATEGORIK = ["Produk"]
TARGET = "Jumlah_Terjual"


# ==========================================
# PELATIHAN MODEL FINAL
# ==========================================

def main():

    print("=" * 55)
    print("PELATIHAN MODEL FINAL VINIX7")
    print("=" * 55)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print("\nJumlah data awal:", len(df))

    # Memastikan kolom tersedia
    kolom_wajib = (
        FITUR_NUMERIK
        + FITUR_KATEGORIK
        + [TARGET, "Bulan"]
    )

    kolom_tidak_ada = [
        kolom for kolom in kolom_wajib
        if kolom not in df.columns
    ]

    if kolom_tidak_ada:
        raise ValueError(
            f"Kolom tidak ditemukan: {kolom_tidak_ada}"
        )

    # Memastikan periode data
    df["Bulan"] = pd.to_datetime(
        df["Bulan"],
        errors="coerce"
    )

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    df[FITUR_NUMERIK] = df[
        FITUR_NUMERIK
    ].apply(pd.to_numeric, errors="coerce")

    # Menghapus data tidak valid
    data_valid = (
        df["Bulan"].notna()
        & df["Produk"].notna()
        & df[TARGET].notna()
        & df[FITUR_NUMERIK].notna().all(axis=1)
    )

    df = df.loc[data_valid].copy()

    if df.empty:
        raise ValueError(
            "Tidak ada data yang valid untuk training."
        )

    # Memastikan data sampai Desember 2025
    periode_awal = df["Bulan"].min()
    periode_akhir = df["Bulan"].max()

    print("Jumlah produk:", df["Produk"].nunique())
    print("Periode awal:", periode_awal.strftime("%B %Y"))
    print("Periode akhir:", periode_akhir.strftime("%B %Y"))

    if periode_akhir < pd.Timestamp("2025-12-01"):
        raise ValueError(
            "Dataset belum mencakup Desember 2025."
        )

    X_train = df[
        FITUR_NUMERIK + FITUR_KATEGORIK
    ].copy()

    y_train = df[TARGET].copy()

    if (y_train < 0).any():
        raise ValueError(
            "Target penjualan mengandung nilai negatif."
        )

    # ======================================
    # ONE-HOT ENCODING
    # ======================================

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "produk",
                OneHotEncoder(handle_unknown="ignore"),
                FITUR_KATEGORIK
            )
        ],
        remainder="passthrough"
    )

    # ======================================
    # EXTRA TREES REGRESSOR
    # ======================================

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            (
                "regressor",
                ExtraTreesRegressor(
                    n_estimators=300,
                    max_features=1.0,
                    min_samples_split=2,
                    min_samples_leaf=1,
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )

    print("\nFitur numerik:", len(FITUR_NUMERIK))
    print("Fitur kategorik:", len(FITUR_KATEGORIK))
    print("Algoritma: Extra Trees Regressor")
    print("Encoding: One-Hot Encoding")

    print("\nMemulai pelatihan model final...")

    model.fit(X_train, y_train)

    # ======================================
    # SIMPAN MODEL FINAL
    # ======================================

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(model, MODEL_PATH)

    print("\nPELATIHAN MODEL FINAL BERHASIL!")
    print("-" * 55)
    print("Jumlah data training:", len(X_train))
    print("Jumlah produk:", X_train["Produk"].nunique())
    print("Periode training:", periode_awal.date(), "sampai", periode_akhir.date())
    print("Model:", MODEL_PATH)


if __name__ == "__main__":
    main()
