
from pathlib import Path
import pandas as pd

# Lokasi project VINIX7
PROJECT_ROOT = Path(__file__).resolve().parents[3]
FILE_PATH = PROJECT_ROOT / "storage" / "raw" / "Data Projek Vinix (1).xlsx"

# Sheet yang digunakan dalam project
SHEET_NAMES = [
    "Data_produksi_pupuk",
    "Data_Bahan_Organik",
    "Data_Produk_Katalog",
    "Data_Penjualan",
    "Data Wilayah_Kalurahan",
    "Data_Wilayah_Padukuhan",
    "Data_Pertanian"
]


def load_raw_data():
    """Membaca dataset sumber VINIX7 dari file Excel."""

    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"File dataset tidak ditemukan: {FILE_PATH}"
        )

    # Periksa ketersediaan sheet
    with pd.ExcelFile(FILE_PATH, engine="openpyxl") as excel:
        sheet_tersedia = excel.sheet_names
        sheet_hilang = [
            sheet for sheet in SHEET_NAMES
            if sheet not in sheet_tersedia
        ]

        if sheet_hilang:
            raise ValueError(
                f"Sheet tidak ditemukan: {sheet_hilang}"
            )

        # Baca hanya 7 sheet yang digunakan
        data = pd.read_excel(
            excel,
            sheet_name=SHEET_NAMES
        )

    # Ringkasan hasil loading
    print("DATA RAW VINIX7 BERHASIL DIMUAT")
    print("=" * 45)

    for nama, df in data.items():
        print(
            f"{nama}: {len(df)} baris, "
            f"{len(df.columns)} kolom"
        )

    return data


if __name__ == "__main__":
    data = load_raw_data()
