
from pathlib import Path

import pandas as pd


# ==========================================================
# KONFIGURASI FOLDER
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_DIR = PROJECT_ROOT / "storage" / "standardized"
OUTPUT_DIR = PROJECT_ROOT / "storage" / "integrated"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# FUNGSI BANTU
# ==========================================================

def load_csv(filename):
    """Membaca dataset hasil standardisasi."""
    path = INPUT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {path}"
        )

    return pd.read_csv(path, dtype="string")


def check_columns(df, columns, dataset_name):
    """Memastikan kolom yang dibutuhkan tersedia."""
    missing = [col for col in columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Kolom {missing} tidak ditemukan di {dataset_name}"
        )


def check_primary_key(df, key, dataset_name):
    """Memastikan primary key tidak kosong atau duplikat."""
    check_columns(df, [key], dataset_name)

    if df[key].isna().any():
        raise ValueError(
            f"{dataset_name}: terdapat {key} kosong."
        )

    if df[key].duplicated().any():
        raise ValueError(
            f"{dataset_name}: terdapat duplikasi {key}."
        )


def check_foreign_key(child, child_key, parent, parent_key, relation):
    """Memeriksa kesesuaian foreign key dengan tabel induk."""
    check_columns(child, [child_key], relation)
    check_columns(parent, [parent_key], relation)

    invalid = child.loc[
        child[child_key].notna()
        & ~child[child_key].isin(parent[parent_key]),
        child_key
    ]

    if not invalid.empty:
        raise ValueError(
            f"Relasi {relation} gagal. "
            f"{len(invalid)} ID tidak ditemukan: "
            f"{invalid.drop_duplicates().tolist()}"
        )


def save_integrated(df, filename, original_rows, dataset_name):
    """Validasi jumlah baris dan menyimpan hasil integrasi."""
    if len(df) != original_rows:
        raise ValueError(
            f"{dataset_name}: jumlah baris berubah "
            f"dari {original_rows} menjadi {len(df)}."
        )

    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8-sig")

    print(
        f"{dataset_name}: {len(df)} baris, "
        f"{len(df.columns)} kolom"
    )
    print(f"Disimpan: {path.name}")


# ==========================================================
# 1. INTEGRASI DATA PERTANIAN
# Pertanian + Padukuhan + Kalurahan
# ==========================================================

def integrate_agriculture(agri, pad, kal):

    check_primary_key(pad, "padukuhan_id", "Padukuhan")
    check_primary_key(kal, "kalurahan_id", "Kalurahan")

    check_foreign_key(
        pad, "kalurahan_id",
        kal, "kalurahan_id",
        "Padukuhan -> Kalurahan"
    )

    check_foreign_key(
        agri, "padukuhan_id",
        pad, "padukuhan_id",
        "Pertanian -> Padukuhan"
    )

    original_rows = len(agri)

    # Ambil informasi padukuhan dan kalurahan.
    pad_columns = [
        "padukuhan_id",
        "kalurahan_id",
        "latitude",
        "longitude"
    ]

    kal_columns = [
        "kalurahan_id",
        "luas_kalurahan_ha",
        "jumlah_padukuhan",
        "jumlah_rw",
        "jumlah_rt",
        "jarak_kecamatan_km",
        "jarak_kabupaten_km",
        "jarak_provinsi_km",
        "jarak_nasional_km"
    ]

    check_columns(pad, pad_columns, "Padukuhan")
    check_columns(kal, kal_columns, "Kalurahan")

    result = agri.merge(
        pad[pad_columns],
        on="padukuhan_id",
        how="left",
        validate="many_to_one"
    )

    result = result.merge(
        kal[kal_columns],
        on="kalurahan_id",
        how="left",
        validate="many_to_one"
    )

    save_integrated(
        result,
        "pertanian_terintegrasi.csv",
        original_rows,
        "Pertanian Terintegrasi"
    )


# ==========================================================
# 2. INTEGRASI DATA BAHAN ORGANIK
# Bahan Organik + Padukuhan + Kalurahan
# ==========================================================

def integrate_organic(bo, pad, kal):

    check_primary_key(pad, "padukuhan_id", "Padukuhan")
    check_primary_key(kal, "kalurahan_id", "Kalurahan")
    check_primary_key(bo, "ketersediaan_id", "Bahan Organik")

    check_foreign_key(
        pad, "kalurahan_id",
        kal, "kalurahan_id",
        "Padukuhan -> Kalurahan"
    )

    check_foreign_key(
        bo, "padukuhan_id",
        pad, "padukuhan_id",
        "Bahan Organik -> Padukuhan"
    )

    original_rows = len(bo)

    pad_columns = [
        "padukuhan_id",
        "kalurahan_id",
        "latitude",
        "longitude"
    ]

    kal_columns = [
        "kalurahan_id",
        "luas_kalurahan_ha",
        "jumlah_padukuhan",
        "jarak_kecamatan_km",
        "latitude",
        "longitude"
    ]

    check_columns(pad, pad_columns, "Padukuhan")
    check_columns(kal, kal_columns, "Kalurahan")

    result = bo.merge(
        pad[pad_columns],
        on="padukuhan_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_padukuhan")
    )

    result = result.merge(
        kal[kal_columns],
        on="kalurahan_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_kalurahan")
    )

    save_integrated(
        result,
        "bahan_organik_terintegrasi.csv",
        original_rows,
        "Bahan Organik Terintegrasi"
    )


# ==========================================================
# 3. INTEGRASI DATA PRODUKSI
# Produksi + Katalog Produk
# ==========================================================

def integrate_production(produksi, produk):

    check_primary_key(produk, "produk_id", "Katalog Produk")

    check_foreign_key(
        produksi, "produk_id",
        produk, "produk_id",
        "Produksi -> Katalog Produk"
    )

    original_rows = len(produksi)

    result = produksi.merge(
        produk,
        left_on="produk_id",
        right_on="produk_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_katalog")
    )

    save_integrated(
        result,
        "produksi_terintegrasi.csv",
        original_rows,
        "Produksi Terintegrasi"
    )


# ==========================================================
# 4. INTEGRASI DATA PENJUALAN
# Penjualan + Katalog Produk
# ==========================================================

def integrate_sales(penjualan, produk):

    check_primary_key(produk, "produk_id", "Katalog Produk")

    check_foreign_key(
        penjualan, "Produk_id",
        produk, "produk_id",
        "Penjualan -> Katalog Produk"
    )

    original_rows = len(penjualan)

    result = penjualan.merge(
        produk,
        left_on="Produk_id",
        right_on="produk_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_katalog")
    )

    save_integrated(
        result,
        "penjualan_terintegrasi.csv",
        original_rows,
        "Penjualan Terintegrasi"
    )


# ==========================================================
# PROSES UTAMA
# ==========================================================

def run_integration():

    print("=" * 55)
    print("DATA INTEGRATION - VINIX7")
    print("=" * 55)

    # Load seluruh dataset standardized.
    kal = load_csv("Data_Wilayah_Kalurahan.csv")
    pad = load_csv("Data_Wilayah_Padukuhan.csv")
    agri = load_csv("Data_Pertanian.csv")
    bo = load_csv("Data_Bahan_Organik.csv")
    produk = load_csv("Data_Produk_Katalog.csv")
    produksi = load_csv("Data_produksi_pupuk.csv")
    penjualan = load_csv("Data_Penjualan.csv")

    print("\nDataset berhasil dimuat.")

    # Jalankan integrasi.
    integrate_agriculture(agri, pad, kal)
    integrate_organic(bo, pad, kal)
    integrate_production(produksi, produk)
    integrate_sales(penjualan, produk)

    print("\n" + "=" * 55)
    print("DATA INTEGRATION VINIX7 BERHASIL")
    print(f"Output folder: {OUTPUT_DIR}")
    print("=" * 55)


if __name__ == "__main__":
    run_integration()
