
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sqlalchemy import text
from database.connection import engine


# ==========================================
# KONFIGURASI PATH
# ==========================================

MODEL_PATH = Path(
    "backend/models/extra_trees_final_2026.pkl"
)

OUTPUT_DIR = Path("storage/machine_learning")

OUTPUT_PATH = (
    OUTPUT_DIR / "hasil_prediksi_2026.csv"
)


# ==========================================
# KONFIGURASI FITUR
# ==========================================

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


# ==========================================
# MENGAMBIL DATA PENJUALAN POSTGRESQL
# ==========================================

def ambil_data_penjualan():

    query = """
        SELECT
            "Bulan",
            "Produk",
            SUM("Jumlah_Terjual") AS "Jumlah_Terjual"
        FROM penjualan
        WHERE "Bulan" <= '2025-12-31'
        GROUP BY "Bulan", "Produk"
        ORDER BY "Produk", "Bulan"
    """

    with engine.connect() as connection:
        df = pd.read_sql(
            text(query),
            connection
        )

    return df


# ==========================================
# PERSIAPAN RIWAYAT PENJUALAN
# ==========================================

def persiapkan_riwayat(df):

    df["Bulan"] = pd.to_datetime(
        df["Bulan"],
        errors="coerce"
    )

    df["Jumlah_Terjual"] = pd.to_numeric(
        df["Jumlah_Terjual"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Bulan", "Produk", "Jumlah_Terjual"]
    )

    df = df.sort_values(
        ["Produk", "Bulan"]
    )

    riwayat_produk = {}

    for produk, data in df.groupby("Produk"):

        data = data.sort_values("Bulan").copy()

        data = data.set_index("Bulan")

        data = data.asfreq("MS")

        data["Jumlah_Terjual"] = (
            data["Jumlah_Terjual"].fillna(0)
        )

        if len(data) < 12:
            raise ValueError(
                f"Riwayat produk {produk} kurang dari 12 bulan."
            )

        if data.index.max() != pd.Timestamp("2025-12-01"):
            raise ValueError(
                f"Data produk {produk} belum sampai Desember 2025."
            )

        riwayat_produk[produk] = (
            data["Jumlah_Terjual"].astype(float).tolist()
        )

    return riwayat_produk


# ==========================================
# MEMBUAT FITUR PREDIKSI
# ==========================================

def buat_fitur(produk, riwayat, tanggal):

    bulan = tanggal.month
    tahun = tanggal.year

    fitur = {
        "lag_1": riwayat[-1],
        "lag_2": riwayat[-2],
        "lag_3": riwayat[-3],
        "lag_12": riwayat[-12],
        "bulan": bulan,
        "tahun": tahun,
        "bulan_sin": np.sin(
            2 * np.pi * bulan / 12
        ),
        "bulan_cos": np.cos(
            2 * np.pi * bulan / 12
        ),
        "Produk": produk,
    }

    return pd.DataFrame(
        [fitur],
        columns=FITUR
    )


# ==========================================
# PREDIKSI TAHUN 2026
# ==========================================

def lakukan_prediksi(model, riwayat_produk):

    hasil_prediksi = []

    periode_prediksi = pd.date_range(
        start="2026-01-01",
        end="2026-12-01",
        freq="MS"
    )

    for produk, riwayat in riwayat_produk.items():

        print(f"\nMemproses produk: {produk}")

        riwayat = riwayat.copy()

        for tanggal in periode_prediksi:

            X_prediksi = buat_fitur(
                produk,
                riwayat,
                tanggal
            )

            nilai_prediksi = float(
                model.predict(X_prediksi)[0]
            )

            # Jumlah penjualan tidak boleh negatif
            nilai_prediksi = max(
                0.0,
                nilai_prediksi
            )

            hasil_prediksi.append({
                "Bulan": tanggal,
                "Produk": produk,
                "Prediksi_Penjualan": nilai_prediksi
            })

            # Prediksi bulan ini menjadi lag
            # untuk bulan berikutnya
            riwayat.append(nilai_prediksi)

    return pd.DataFrame(hasil_prediksi)


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("=" * 55)
    print("PREDIKSI PENJUALAN VINIX7 TAHUN 2026")
    print("=" * 55)

    # Memeriksa model
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model final tidak ditemukan: {MODEL_PATH}"
        )

    # Memuat model final
    print("\nMemuat model final...")

    model = joblib.load(MODEL_PATH)

    # Mengambil data PostgreSQL
    print("Mengambil data penjualan PostgreSQL...")

    df = ambil_data_penjualan()

    print("Jumlah data historis:", len(df))

    # Menyiapkan riwayat produk
    riwayat_produk = persiapkan_riwayat(df)

    print("Jumlah produk:", len(riwayat_produk))

    # Membuat prediksi
    print("\nMemulai prediksi tahun 2026...")

    hasil = lakukan_prediksi(
        model,
        riwayat_produk
    )

    # Memastikan jumlah hasil prediksi
    jumlah_diharapkan = len(riwayat_produk) * 12

    if len(hasil) != jumlah_diharapkan:
        raise ValueError(
            "Jumlah hasil prediksi tidak sesuai."
        )

    # Mengurutkan hasil
    hasil = hasil.sort_values(
        ["Bulan", "Produk"]
    ).reset_index(drop=True)

    # Menyimpan CSV
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    hasil_simpan = hasil.copy()

    hasil_simpan["Bulan"] = (
        hasil_simpan["Bulan"].dt.strftime("%Y-%m-%d")
    )

    hasil_simpan["Prediksi_Penjualan"] = (
        hasil_simpan["Prediksi_Penjualan"].round(2)
    )

    hasil_simpan.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # Ringkasan
    print("\nHASIL PREDIKSI 2026")
    print("-" * 55)

    print("Jumlah produk:", hasil["Produk"].nunique())
    print("Jumlah bulan: 12")
    print("Total baris prediksi:", len(hasil))

    print(
        "Total prediksi seluruh produk:",
        round(hasil["Prediksi_Penjualan"].sum(), 2)
    )

    print("\nRingkasan prediksi per produk:")

    ringkasan = (
        hasil.groupby("Produk")["Prediksi_Penjualan"]
        .sum()
        .reset_index()
        .sort_values(
            "Prediksi_Penjualan",
            ascending=False
        )
    )

    print(
        ringkasan.round(2).to_string(index=False)
    )

    print("\nFile hasil prediksi tersimpan di:")
    print(OUTPUT_PATH)

    print("\nPREDIKSI TAHUN 2026 SELESAI!")


if __name__ == "__main__":
    main()
