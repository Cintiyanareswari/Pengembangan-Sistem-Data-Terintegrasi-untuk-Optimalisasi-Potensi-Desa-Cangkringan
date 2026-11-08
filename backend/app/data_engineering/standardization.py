
from pathlib import Path
import sys
import pandas as pd

# Menentukan folder utama proyek VINIX7
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Menambahkan folder utama proyek ke Python path
sys.path.insert(0, str(PROJECT_ROOT))

# Import modul proyek
from backend.app.data_engineering.load_data import load_raw_data
from backend.app.data_engineering.cleaning import clean_data

OUTPUT_DIR = PROJECT_ROOT / "storage" / "standardized"




def standardize_data(data_clean):
    """Standardisasi tujuh dataset VINIX7."""

    data_std = {
        nama: df.copy()
        for nama, df in data_clean.items()
    }

    # 1. Standardisasi teks
    for df in data_std.values():
        for col in df.select_dtypes(
            include=["object", "string"]
        ).columns:
            df[col] = df[col].astype("string").str.strip()

    # 2. Standardisasi data produksi
    prod = data_std["Data_produksi_pupuk"]

    kolom_produksi = {
        "jumlah_bahan_baku": (
            "nilai_bahan_baku",
            "satuan_bahan_baku"
        ),
        "Stok": (
            "nilai_stok",
            "satuan_stok"
        )
    }

    for sumber, (kolom_nilai, kolom_satuan) in kolom_produksi.items():

        teks = prod[sumber].astype("string").str.strip()

        prod[kolom_satuan] = (
            teks.str.extract(r"([A-Za-z]+)\s*$")[0]
            .astype("string")
        )

        nilai = (
            teks.str.replace(
                r"\s*[A-Za-z]+\s*$", "", regex=True
            )
            .str.strip()
            .str.replace(".", "", regex=False)
        )

        prod[kolom_nilai] = pd.to_numeric(
            nilai, errors="raise"
        ).astype("Int64")

    # 3. Standardisasi satuan
    for nama in ["Data_produksi_pupuk", "Data_Penjualan"]:
        df = data_std[nama]

        if "Satuan" in df.columns:
            df["Satuan"] = df["Satuan"].replace({
                "L": "Liter"
            })

    # 4. Standardisasi tipe data numerik
    numerik = {
        "Data Wilayah_Kalurahan": [
            "luas_kalurahan_ha",
            "jumlah_padukuhan",
            "jumlah_rw",
            "jumlah_rt",
            "jarak_kecamatan_km",
            "jarak_kabupaten_km",
            "jarak_provinsi_km",
            "jarak_nasional_km",
            "latitude",
            "longitude"
        ],
        "Data_Wilayah_Padukuhan": [
            "jumlah_rt",
            "jumlah_rw",
            "latitude",
            "longitude"
        ],
        "Data_Pertanian": [
            "tahun",
            "luas_panen_ha",
            "luas_lahan_ha",
            "jumlah_petani",
            "jumlah_utp",
            "jumlah_kelompok_tani",
            "produksi"
        ],
        "Data_Bahan_Organik": [
            "jumlah_ketersediaan",
            "jarak_ke_produksi_km",
            "jumlah_sumber"
        ]
    }

    for nama, kolom in numerik.items():
        for col in kolom:
            data_std[nama][col] = pd.to_numeric(
                data_std[nama][col],
                errors="raise"
            )

    # 5. Standardisasi periode
    data_std["Data_Bahan_Organik"]["periode"] = (
        pd.to_datetime(
            data_std["Data_Bahan_Organik"]["periode"],
            errors="raise"
        )
    )

    # 6. Validasi konsistensi produk
    prod = data_std["Data_produksi_pupuk"]
    jual = data_std["Data_Penjualan"]
    katalog = data_std["Data_Produk_Katalog"]

    assert set(prod["produk_id"].dropna()) == set(
        jual["Produk_id"].dropna()
    ), "ID produk produksi dan penjualan tidak konsisten."

    assert set(jual["Produk"].dropna()) == set(
        katalog["Nama_Produk"].dropna()
    ), "Nama produk penjualan dan katalog tidak konsisten."

    # 7. Validasi relasi wilayah
    pad = data_std["Data_Wilayah_Padukuhan"]
    kal = data_std["Data Wilayah_Kalurahan"]

    assert set(pad["kalurahan_id"]).issubset(
        set(kal["kalurahan_id"])
    ), "Ada kalurahan_id yang tidak ditemukan."

    mapping = kal.set_index("kalurahan_id")["kalurahan"]

    assert (
        pad["kalurahan"].reset_index(drop=True)
        == pad["kalurahan_id"].map(mapping).reset_index(drop=True)
    ).all(), "Nama kalurahan tidak sesuai dengan ID."

    assert set(
        data_std["Data_Bahan_Organik"]["padukuhan_id"]
    ).issubset(set(pad["padukuhan_id"])), (
        "Ada padukuhan_id bahan organik yang tidak ditemukan."
    )

    assert set(
        data_std["Data_Pertanian"]["padukuhan_id"]
    ).issubset(set(pad["padukuhan_id"])), (
        "Ada padukuhan_id pertanian yang tidak ditemukan."
    )

    # 8. Validasi hasil standardisasi
    for nama, df in data_std.items():

        assert len(df) == len(data_clean[nama]), (
            f"Jumlah baris berubah: {nama}"
        )

        assert df.isna().sum().sum() == 0, (
            f"Ada missing value: {nama}"
        )

    print("Standardisasi VINIX7 berhasil.")

    return data_std


def save_standardized_data(data_std):
    """Menyimpan hasil standardisasi ke CSV."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for nama, df in data_std.items():

        path = OUTPUT_DIR / f"{nama.replace(' ', '_')}.csv"

        df.to_csv(
            path,
            index=False,
            encoding="utf-8-sig"
        )

        cek = pd.read_csv(path)

        assert df.shape == cek.shape, (
            f"Verifikasi gagal: {nama}"
        )

        print(f"{path.name}: {df.shape} | OK")

    print(f"\nData tersimpan di: {OUTPUT_DIR}")

data = load_raw_data()
data_clean = clean_data(data)

data_std = standardize_data(data_clean)
save_standardized_data(data_std)
