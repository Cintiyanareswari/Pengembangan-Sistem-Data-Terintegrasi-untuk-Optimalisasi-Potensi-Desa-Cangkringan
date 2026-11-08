
from pathlib import Path
import pandas as pd

# =====================================================
# 1. PATH PROJECT
# =====================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

STANDARDIZED_DIR = ROOT_DIR / "storage" / "standardized"
INTEGRATED_DIR = ROOT_DIR / "storage" / "integrated"
REPORT_DIR = ROOT_DIR / "storage" / "validation"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# 2. KONFIGURASI DATA
# =====================================================

STANDARDIZED_FILES = {
    "produksi": "Data_produksi_pupuk",
    "organik": "Data_Bahan_Organik",
    "katalog": "Data_Produk_Katalog",
    "penjualan": "Data_Penjualan",
    "kalurahan": "Data_Wilayah_Kalurahan",
    "padukuhan": "Data_Wilayah_Padukuhan",
    "pertanian": "Data_Pertanian",
}

INTEGRATED_FILES = {
    "pertanian_integrasi": "pertanian_terintegrasi",
    "organik_integrasi": "bahan_organik_terintegrasi",
    "produksi_integrasi": "produksi_terintegrasi",
    "penjualan_integrasi": "penjualan_terintegrasi",
}

PRIMARY_KEYS = {
    "produksi": "produksi_id",
    "organik": "ketersediaan_id",
    "katalog": "produk_id",
    "penjualan": "Penjualan_id",
    "kalurahan": "kalurahan_id",
    "padukuhan": "padukuhan_id",
    "pertanian": "agri_id",
}

EXPECTED_ROWS = {
    "produksi": 66,
    "organik": 88,
    "katalog": 11,
    "penjualan": 792,
    "kalurahan": 5,
    "padukuhan": 73,
    "pertanian": 511,
}


# =====================================================
# 3. PENAMPUNG HASIL VALIDASI
# =====================================================

results = []


def add_result(category, dataset, check, status, detail):
    results.append({
        "kategori": category,
        "dataset": dataset,
        "pemeriksaan": check,
        "status": status,
        "detail": detail
    })


# =====================================================
# 4. MEMUAT DATA CSV
# =====================================================

def load_data(folder, filename, category):
    path = folder / f"{filename}.csv"

    if not path.exists():
        add_result(
            category,
            filename,
            "File tersedia",
            "GAGAL",
            f"File tidak ditemukan: {path}"
        )
        return None

    try:
        df = pd.read_csv(path, dtype="string")

        add_result(
            category,
            filename,
            "File tersedia",
            "LOLOS",
            f"{len(df)} baris dan {len(df.columns)} kolom"
        )

        return df

    except Exception as e:
        add_result(
            category,
            filename,
            "Pembacaan file",
            "GAGAL",
            str(e)
        )
        return None


# =====================================================
# 5. VALIDASI PRIMARY KEY
# =====================================================

def validate_primary_key(df, dataset, key):

    if key not in df.columns:
        add_result(
            "Primary Key",
            dataset,
            key,
            "GAGAL",
            "Kolom primary key tidak ditemukan"
        )
        return

    values = df[key].str.strip()

    missing = values.isna() | values.eq("")
    duplicates = values.duplicated(keep=False)

    if missing.any():
        add_result(
            "Primary Key",
            dataset,
            key,
            "GAGAL",
            f"Terdapat {missing.sum()} nilai kosong"
        )

    elif duplicates.any():
        add_result(
            "Primary Key",
            dataset,
            key,
            "GAGAL",
            f"Terdapat {duplicates.sum()} baris dengan ID duplikat"
        )

    else:
        add_result(
            "Primary Key",
            dataset,
            key,
            "LOLOS",
            "ID lengkap dan unik"
        )


# =====================================================
# 6. VALIDASI FOREIGN KEY
# =====================================================

def validate_foreign_key(
    child_df,
    child_name,
    child_column,
    parent_df,
    parent_name,
    parent_column
):

    if child_column not in child_df.columns:
        add_result(
            "Foreign Key",
            child_name,
            child_column,
            "GAGAL",
            "Kolom foreign key tidak ditemukan"
        )
        return

    if parent_column not in parent_df.columns:
        add_result(
            "Foreign Key",
            child_name,
            child_column,
            "GAGAL",
            f"Kolom referensi {parent_name}.{parent_column} tidak ditemukan"
        )
        return

    child_values = child_df[child_column].str.strip()
    parent_values = parent_df[parent_column].str.strip()

    missing = child_values.isna() | child_values.eq("")

    parent_set = set(parent_values.dropna())

    invalid = (
        child_values.notna()
        & child_values.ne("")
        & ~child_values.isin(parent_set)
    )

    if missing.any():
        add_result(
            "Foreign Key",
            child_name,
            child_column,
            "GAGAL",
            f"Terdapat {missing.sum()} nilai foreign key kosong"
        )

    elif invalid.any():
        invalid_values = child_values[invalid].unique().tolist()

        add_result(
            "Foreign Key",
            child_name,
            child_column,
            "GAGAL",
            f"{invalid.sum()} baris tidak memiliki referensi valid. "
            f"Contoh: {invalid_values[:10]}"
        )

    else:
        add_result(
            "Foreign Key",
            child_name,
            child_column,
            "LOLOS",
            f"Semua nilai terhubung ke tabel {parent_name}"
        )


# =====================================================
# 7. VALIDASI NILAI KOSONG
# =====================================================

def validate_missing_values(df, dataset):

    missing_count = df.isna().sum().sum()

    if missing_count > 0:
        columns = df.isna().sum()
        columns = columns[columns > 0].to_dict()

        add_result(
            "Kelengkapan",
            dataset,
            "Nilai kosong",
            "PERIKSA",
            f"Terdapat {missing_count} nilai kosong: {columns}"
        )

    else:
        add_result(
            "Kelengkapan",
            dataset,
            "Nilai kosong",
            "LOLOS",
            "Tidak ditemukan nilai kosong"
        )


# =====================================================
# 8. VALIDASI JUMLAH BARIS
# =====================================================

def validate_row_count(df, dataset, expected):

    actual = len(df)

    if actual == expected:
        add_result(
            "Jumlah Data",
            dataset,
            "Jumlah baris",
            "LOLOS",
            f"{actual} baris sesuai jumlah yang diharapkan"
        )

    else:
        add_result(
            "Jumlah Data",
            dataset,
            "Jumlah baris",
            "GAGAL",
            f"Diharapkan {expected} baris, ditemukan {actual} baris"
        )


# =====================================================
# 9. VALIDASI DUPLIKASI BARIS
# =====================================================

def validate_duplicate_rows(df, dataset):

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        add_result(
            "Duplikasi",
            dataset,
            "Duplikasi baris",
            "PERIKSA",
            f"Ditemukan {duplicate_count} baris duplikat"
        )

    else:
        add_result(
            "Duplikasi",
            dataset,
            "Duplikasi baris",
            "LOLOS",
            "Tidak ditemukan baris duplikat penuh"
        )


# =====================================================
# 10. VALIDASI STRUKTUR KOLOM
# =====================================================

def validate_integrated_columns(df, dataset, required_columns):

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        add_result(
            "Struktur",
            dataset,
            "Kolom integrasi",
            "GAGAL",
            f"Kolom tidak ditemukan: {missing_columns}"
        )

    else:
        add_result(
            "Struktur",
            dataset,
            "Kolom integrasi",
            "LOLOS",
            "Semua kolom wajib tersedia"
        )


# =====================================================
# 11. PROSES UTAMA VALIDASI
# =====================================================

def main():

    standardized = {}
    integrated = {}

    print("\n")
    print("=" * 55)
    print("VALIDATION DATA VINIX7")
    print("=" * 55)

    # -------------------------------------------------
    # A. LOAD STANDARDIZED DATA
    # -------------------------------------------------

    print("\nMEMUAT DATA STANDARDIZED")

    for name, filename in STANDARDIZED_FILES.items():

        df = load_data(
            STANDARDIZED_DIR,
            filename,
            "Standardized"
        )

        if df is not None:

            standardized[name] = df

            validate_primary_key(
                df,
                name,
                PRIMARY_KEYS[name]
            )

            validate_row_count(
                df,
                name,
                EXPECTED_ROWS[name]
            )

            validate_missing_values(
                df,
                name
            )

            validate_duplicate_rows(
                df,
                name
            )

    # -------------------------------------------------
    # B. LOAD INTEGRATED DATA
    # -------------------------------------------------

    print("\nMEMUAT DATA INTEGRATED")

    for name, filename in INTEGRATED_FILES.items():

        df = load_data(
            INTEGRATED_DIR,
            filename,
            "Integrated"
        )

        if df is not None:
            integrated[name] = df

    # -------------------------------------------------
    # C. FOREIGN KEY STANDARDIZED
    # -------------------------------------------------

    print("\nVALIDASI FOREIGN KEY STANDARDIZED")

    # Pertanian -> Padukuhan
    if "pertanian" in standardized and "padukuhan" in standardized:
        validate_foreign_key(
            standardized["pertanian"],
            "pertanian",
            "padukuhan_id",
            standardized["padukuhan"],
            "padukuhan",
            "padukuhan_id"
        )

    # Organik -> Padukuhan
    if "organik" in standardized and "padukuhan" in standardized:
        validate_foreign_key(
            standardized["organik"],
            "organik",
            "padukuhan_id",
            standardized["padukuhan"],
            "padukuhan",
            "padukuhan_id"
        )

    # Produksi -> Katalog
    if "produksi" in standardized and "katalog" in standardized:
        validate_foreign_key(
            standardized["produksi"],
            "produksi",
            "produk_id",
            standardized["katalog"],
            "katalog",
            "produk_id"
        )

    # Penjualan -> Katalog
    if "penjualan" in standardized and "katalog" in standardized:
        validate_foreign_key(
            standardized["penjualan"],
            "penjualan",
            "Produk_id",
            standardized["katalog"],
            "katalog",
            "produk_id"
        )

    # -------------------------------------------------
    # D. FOREIGN KEY INTEGRATED
    # -------------------------------------------------

    print("\nVALIDASI FOREIGN KEY INTEGRATED")

    # Pertanian terintegrasi -> Kalurahan
    if "pertanian_integrasi" in integrated and "kalurahan" in standardized:
        validate_foreign_key(
            integrated["pertanian_integrasi"],
            "pertanian_integrasi",
            "kalurahan_id",
            standardized["kalurahan"],
            "kalurahan",
            "kalurahan_id"
        )

    # Bahan organik terintegrasi -> Kalurahan
    if "organik_integrasi" in integrated and "kalurahan" in standardized:
        validate_foreign_key(
            integrated["organik_integrasi"],
            "organik_integrasi",
            "kalurahan_id",
            standardized["kalurahan"],
            "kalurahan",
            "kalurahan_id"
        )

    # -------------------------------------------------
    # E. VALIDASI DATA INTEGRATED
    # -------------------------------------------------

    print("\nVALIDASI DATA INTEGRATED")

    integrated_checks = {
        "pertanian_integrasi": {
            "rows": 511,
            "key": "agri_id",
            "columns": [
                "agri_id",
                "padukuhan_id",
                "kalurahan_id",
                "latitude",
                "longitude",
                "luas_kalurahan_ha"
            ]
        },

        "organik_integrasi": {
            "rows": 88,
            "key": "ketersediaan_id",
            "columns": [
                "ketersediaan_id",
                "bahan_id",
                "padukuhan_id",
                "kalurahan_id"
            ]
        },

        "produksi_integrasi": {
            "rows": 66,
            "key": "produksi_id",
            "columns": [
                "produksi_id",
                "produk_id",
                "Nama_Produk_katalog",
                "Jenis_Produk_katalog"
            ]
        },

        "penjualan_integrasi": {
            "rows": 792,
            "key": "Penjualan_id",
            "columns": [
                "Penjualan_id",
                "Produk_id",
                "produk_id",
                "Nama_Produk"
            ]
        }
    }

    for name, config in integrated_checks.items():

        if name not in integrated:
            continue

        df = integrated[name]

        validate_row_count(
            df,
            name,
            config["rows"]
        )

        validate_primary_key(
            df,
            name,
            config["key"]
        )

        validate_integrated_columns(
            df,
            name,
            config["columns"]
        )

        validate_duplicate_rows(
            df,
            name
        )

    # -------------------------------------------------
    # F. SIMPAN LAPORAN VALIDASI
    # -------------------------------------------------

    report = pd.DataFrame(results)

    report_path = REPORT_DIR / "validation_report.csv"

    report.to_csv(
        report_path,
        index=False,
        encoding="utf-8-sig"
    )

    # -------------------------------------------------
    # G. TAMPILKAN HASIL
    # -------------------------------------------------

    print("\n")
    print("=" * 55)
    print("HASIL VALIDASI DATA VINIX7")
    print("=" * 55)

    if not report.empty:

        print(report.to_string(index=False))

        passed = (report["status"] == "LOLOS").sum()
        failed = (report["status"] == "GAGAL").sum()
        review = (report["status"] == "PERIKSA").sum()

        print("\n")
        print("-" * 55)
        print(f"Total pemeriksaan : {len(report)}")
        print(f"LOLOS             : {passed}")
        print(f"GAGAL             : {failed}")
        print(f"PERLU DIPERIKSA   : {review}")
        print("-" * 55)

        if failed == 0 and review == 0:
            print("SEMUA PEMERIKSAAN BERHASIL")

        elif failed == 0:
            print("VALIDASI SELESAI, ADA DATA YANG PERLU DITINJAU")

        else:
            print("VALIDASI SELESAI, MASIH ADA KESALAHAN")

    print("\nLaporan tersimpan di:")
    print(report_path)


# =====================================================
# 12. EKSEKUSI PROGRAM
# =====================================================

if __name__ == "__main__":
    main()
