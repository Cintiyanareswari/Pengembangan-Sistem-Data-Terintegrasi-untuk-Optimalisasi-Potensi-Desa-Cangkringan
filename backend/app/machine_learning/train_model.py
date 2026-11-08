
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

TRAIN_PATH = DATA_DIR / "data_train.csv"
MODEL_PATH = MODEL_DIR / "extra_trees_model.pkl"


# ==========================================
# KONFIGURASI FITUR
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
# PELATIHAN MODEL
# ==========================================

def main():

    print("=" * 50)
    print("PELATIHAN MODEL EXTRA TREES VINIX7")
    print("=" * 50)

    # Memastikan file training tersedia
    if not TRAIN_PATH.exists():
        raise FileNotFoundError(
            f"Data training tidak ditemukan: {TRAIN_PATH}"
        )

    # Membaca data training
    df = pd.read_csv(TRAIN_PATH)

    print("\nJumlah data training:", len(df))
    print("Jumlah produk:", df["Produk"].nunique())

    # Memastikan kolom yang dibutuhkan tersedia
    kolom_wajib = FITUR_NUMERIK + FITUR_KATEGORIK + [TARGET]

    kolom_tidak_ada = [
        kolom for kolom in kolom_wajib
        if kolom not in df.columns
    ]

    if kolom_tidak_ada:
        raise ValueError(
            f"Kolom berikut tidak ditemukan: {kolom_tidak_ada}"
        )

    # Memisahkan fitur dan target
    X_train = df[FITUR_NUMERIK + FITUR_KATEGORIK].copy()
    y_train = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    # Memastikan data numerik valid
    X_train[FITUR_NUMERIK] = X_train[
        FITUR_NUMERIK
    ].apply(pd.to_numeric, errors="coerce")

    data_valid = (
        X_train.notna().all(axis=1)
        & y_train.notna()
    )

    X_train = X_train.loc[data_valid]
    y_train = y_train.loc[data_valid]

    if len(X_train) == 0:
        raise ValueError("Tidak ada data training yang valid.")

    # ======================================
    # PREPROCESSING ONE-HOT ENCODING
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
    # PIPELINE EXTRA TREES
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
    print("Memulai pelatihan model...")

    # Melatih seluruh pipeline
    model.fit(X_train, y_train)

    # Menyimpan model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\nPELATIHAN MODEL SELESAI!")
    print("-" * 50)
    print("Algoritma: Extra Trees Regressor")
    print("Jumlah estimator: 300")
    print("Jumlah data training:", len(X_train))
    print("Jumlah produk:", X_train["Produk"].nunique())
    print("Encoding produk: One-Hot Encoding")
    print("Model tersimpan di:", MODEL_PATH)


if __name__ == "__main__":
    main()
