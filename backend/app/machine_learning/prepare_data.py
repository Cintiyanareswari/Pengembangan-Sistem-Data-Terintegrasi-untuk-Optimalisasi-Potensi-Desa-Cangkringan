
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

OUTPUT_DIR = Path("storage/machine_learning")


def ambil_data_penjualan():
    query = """
        SELECT
            "Bulan",
            "Produk",
            "Jumlah_Terjual"
        FROM penjualan
        ORDER BY "Produk", "Bulan"
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    return df


def persiapkan_data(df):
    df["Bulan"] = pd.to_datetime(df["Bulan"], errors="coerce")
    df["Jumlah_Terjual"] = pd.to_numeric(
        df["Jumlah_Terjual"], errors="coerce"
    )

    df = df.dropna(
        subset=["Bulan", "Produk", "Jumlah_Terjual"]
    )

    df = df.sort_values(["Produk", "Bulan"])

    # Agregasi jika terdapat lebih dari satu catatan
    # untuk produk dan bulan yang sama
    df = (
        df.groupby(["Produk", "Bulan"], as_index=False)
        ["Jumlah_Terjual"].sum()
    )

    hasil = []

    for produk, data in df.groupby("Produk"):
        data = data.sort_values("Bulan").copy()

        # Membuat urutan bulan lengkap
        data = data.set_index("Bulan").asfreq("MS")

        data["Produk"] = produk
        data["Jumlah_Terjual"] = data["Jumlah_Terjual"].fillna(0)

        # Fitur historis penjualan
        for lag in [1, 2, 3, 12]:
            data[f"lag_{lag}"] = (
                data["Jumlah_Terjual"].shift(lag)
            )

        # Fitur kalender
        data["bulan"] = data.index.month
        data["tahun"] = data.index.year

        data["bulan_sin"] = (
            __import__("numpy").sin(
                2 * __import__("numpy").pi * data["bulan"] / 12
            )
        )

        data["bulan_cos"] = (
            __import__("numpy").cos(
                2 * __import__("numpy").pi * data["bulan"] / 12
            )
        )

        data["Bulan"] = data.index

        hasil.append(data.reset_index(drop=True))

    data_model = pd.concat(hasil, ignore_index=True)

    # Menghapus baris yang belum memiliki histori 12 bulan
    data_model = data_model.dropna(
        subset=["lag_1", "lag_2", "lag_3", "lag_12"]
    )

    data_model = data_model.sort_values(
        ["Bulan", "Produk"]
    ).reset_index(drop=True)

    return data_model


def main():
    print("=" * 50)
    print("PERSIAPAN DATA MACHINE LEARNING VINIX7")
    print("=" * 50)

    # 1. Mengambil data dari PostgreSQL
    df = ambil_data_penjualan()

    print("\nJumlah data awal:", len(df))
    print("Jumlah produk:", df["Produk"].nunique())

    # 2. Persiapan fitur dan target
    data_model = persiapkan_data(df)

    # 3. Pembagian data berdasarkan waktu
    data_train = data_model[
        data_model["Bulan"].dt.year <= 2024
    ].copy()

    data_test = data_model[
        data_model["Bulan"].dt.year == 2025
    ].copy()

    # 4. Simpan hasil persiapan data
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data_model.to_csv(
        OUTPUT_DIR / "dataset_model.csv",
        index=False
    )

    data_train.to_csv(
        OUTPUT_DIR / "data_train.csv",
        index=False
    )

    data_test.to_csv(
        OUTPUT_DIR / "data_test.csv",
        index=False
    )

    print("\nHASIL PERSIAPAN DATA")
    print("-" * 50)
    print("Jumlah data siap model:", len(data_model))
    print("Data training:", len(data_train))
    print("Data testing:", len(data_test))
    print("Periode training: sampai Desember 2024")
    print("Periode testing: Januari–Desember 2025")

    print("\nFile tersimpan di:", OUTPUT_DIR)
    print("\nPERSIAPAN DATA SELESAI!")


if __name__ == "__main__":
    main()
