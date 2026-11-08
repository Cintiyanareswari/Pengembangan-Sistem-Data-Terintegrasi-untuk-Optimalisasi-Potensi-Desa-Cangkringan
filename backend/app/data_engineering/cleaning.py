
from pathlib import Path
from datetime import datetime
import pandas as pd

# Lokasi penyimpanan
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "storage" / "processed"


def clean_data(data):
    """Membersihkan seluruh dataset VINIX7."""

    data_clean = {
        nama: df.copy()
        for nama, df in data.items()
    }

    # 1. Membersihkan whitespace pada kolom teks
    for df in data_clean.values():
        for kolom in df.select_dtypes(include="object").columns:
            df[kolom] = df[kolom].apply(
                lambda x: x.strip() if isinstance(x, str) else x
            )

    # 2. Menyamakan tipe data kolom ID
    kolom_id = {
        "Data_produksi_pupuk": ["produksi_id", "produk_id"],
        "Data_Bahan_Organik": [
            "bahan_id", "ketersediaan_id", "padukuhan_id"
        ],
        "Data_Penjualan": ["Penjualan_id", "Produk_id"],
        "Data Wilayah_Kalurahan": ["kalurahan_id"],
        "Data_Wilayah_Padukuhan": ["padukuhan_id", "kalurahan_id"],
        "Data_Pertanian": ["agri_id", "padukuhan_id"]
    }

    for nama, kolom_list in kolom_id.items():
        for kolom in kolom_list:
            if kolom in data_clean[nama].columns:
                data_clean[nama][kolom] = (
                    data_clean[nama][kolom].astype("string").str.strip()
                )

    # 3. Cleaning jarak bahan organik
    df = data_clean["Data_Bahan_Organik"]

    df["jarak_ke_produksi_km"] = df[
        "jarak_ke_produksi_km"
    ].apply(
        lambda x: pd.NA if isinstance(x, (pd.Timestamp, datetime)) else x
    )

    df["jarak_ke_produksi_km"] = pd.to_numeric(
        df["jarak_ke_produksi_km"], errors="coerce"
    )

    # 4. Perbaikan jarak kecamatan yang salah terbaca
    df = data_clean["Data Wilayah_Kalurahan"]

    df.loc[
        df["kalurahan_id"] == "KAL-002",
        "jarak_kecamatan_km"
    ] = 2.7

    df["jarak_kecamatan_km"] = pd.to_numeric(
        df["jarak_kecamatan_km"], errors="coerce"
    )

    # 5. Validasi perhitungan penjualan
    df = data_clean["Data_Penjualan"]

    total_hitung = df["Jumlah_Terjual"] * df["Harga_Satuan"]

    if not total_hitung.equals(df["Total_Penjualan"]):
        raise ValueError("Terdapat ketidaksesuaian total penjualan.")

    print("Proses cleaning berhasil.")
    return data_clean


def save_clean_data(data_clean):
    """Menyimpan dataset hasil cleaning ke CSV."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for nama, df in data_clean.items():
        nama_file = nama.replace(" ", "_") + ".csv"
        path = OUTPUT_DIR / nama_file

        df.to_csv(path, index=False, encoding="utf-8-sig")

        # Verifikasi hasil penyimpanan
        df_check = pd.read_csv(path)

        if df.shape != df_check.shape:
            raise ValueError(f"Verifikasi gagal: {nama_file}")

        print(f"{nama_file}: {df.shape} | OK")

    print(f"\nData tersimpan di: {OUTPUT_DIR}")


if __name__ == "__main__":

    # Import otomatis sesuai cara file dijalankan
    if __package__:
        from .load_data import load_raw_data
    else:
        from load_data import load_raw_data

    data = load_raw_data()
    data_clean = clean_data(data)
    save_clean_data(data_clean)


