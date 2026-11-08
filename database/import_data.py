
import pandas as pd
from pathlib import Path

from database.connection import SessionLocal
from database.models import (
    Kalurahan,
    Padukuhan,
    Pertanian,
    BahanOrganik,
    KetersediaanBahan,
    Produk,
    Produksi,
    Penjualan,
)


# Lokasi sumber CSV
DATA_DIR = Path("storage/standardized")


def import_csv(
    session,
    filename,
    model,
    column_mapping=None,
    drop_columns=None,
    unique_column=None,
    date_columns=None,
):
    """
    Membaca CSV dan memasukkan datanya ke tabel PostgreSQL.
    """

    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")

    # Menghapus kolom yang tidak digunakan oleh model
    if drop_columns:
        df = df.drop(columns=drop_columns, errors="raise")

    # Mengganti nama kolom CSV menjadi atribut model
    if column_mapping:
        df = df.rename(columns=column_mapping)

    # Menghilangkan duplikasi berdasarkan primary key
    if unique_column:
        df = df.drop_duplicates(subset=[unique_column])

    # Mengubah kolom tanggal
    if date_columns:
        for column in date_columns:
            df[column] = pd.to_datetime(
                df[column], errors="coerce"
            ).dt.date

    # Memastikan kolom sesuai dengan atribut model
    model_columns = {
        column.key for column in model.__mapper__.column_attrs
    }

    csv_columns = set(df.columns)

    unknown_columns = csv_columns - model_columns

    if unknown_columns:
        raise ValueError(
            f"Kolom tidak dikenal untuk {model.__name__}: "
            f"{unknown_columns}"
        )

    # Mengubah nilai kosong menjadi None
    df = df.astype(object).where(pd.notna(df), None)

    records = df.to_dict(orient="records")

    # Merge membuat proses import bisa dijalankan ulang
    for record in records:
        session.merge(model(**record))

    session.commit()

    print(
        f"Berhasil: {filename} "
        f"-> tabel {model.__tablename__} "
        f"({len(records)} baris)"
    )


def main():

    session = SessionLocal()

    try:
        print("=" * 55)
        print("MEMULAI IMPORT DATA VINIX7")
        print("=" * 55)

        # 1. KALURAHAN
        import_csv(
            session,
            "Data_Wilayah_Kalurahan.csv",
            Kalurahan,
        )

        # 2. PADUKUHAN
        import_csv(
            session,
            "Data_Wilayah_Padukuhan.csv",
            Padukuhan,
            column_mapping={
                "padukuhan": "nama_padukuhan",
            },
        )

        # 3. BAHAN ORGANIK
        # Satu bahan dapat muncul pada banyak catatan ketersediaan.
        # Karena itu, master bahan harus dibuat unik berdasarkan bahan_id.
        import_csv(
            session,
            "Data_Bahan_Organik.csv",
            BahanOrganik,
            unique_column="bahan_id",
            drop_columns=[
                "ketersediaan_id",
                "padukuhan_id",
                "periode",
                "jumlah_ketersediaan",
                "satuan",
                "kontinuitas",
                "jarak_ke_produksi_km",
                "kemudahan_pengumpulan",
                "status_pemanfaatan",
                "frekuensi",
                "musim",
                "jumlah_sumber",
                "status_data",
            ],
        )

        # 4. PRODUK
        import_csv(
            session,
            "Data_Produk_Katalog.csv",
            Produk,
            column_mapping={
                "Nama_Produk": "nama_produk",
                "Jenis_Produk": "jenis_produk",
                "Deskripsi": "deskripsi",
                "Manfaat": "manfaat",
                "Harga": "harga",
                "Ukuran_Kemasan": "ukuran_kemasan",
                "Produsen": "produsen",
                "Lokasi_Produsen": "lokasi_produsen",
                "Kontak": "kontak",
                "Stok_Ketersediaan": "stok_ketersediaan",
                "Foto Produk": "foto_produk",
            },
        )

        # 5. PERTANIAN
        import_csv(
            session,
            "Data_Pertanian.csv",
            Pertanian,
            column_mapping={
                "padukuhan": "nama_padukuhan",
            },
        )

        # 6. KETERSEDIAAN BAHAN
        import_csv(
            session,
            "Data_Bahan_Organik.csv",
            KetersediaanBahan,
            drop_columns=[
                "jenis_bahan_organik",
                "kategori_bahan",
            ],
            date_columns=["periode"],
        )

        # 7. PRODUKSI
        import_csv(
            session,
            "Data_produksi_pupuk.csv",
            Produksi,
            column_mapping={
                "Nama_Produk": "nama_produk",
                "Jenis_Produk": "jenis_produk",
                "Jumlah_produksi_varian": "jumlah_produksi_varian",
                "Jumlah_produksi_total": "jumlah_produksi_total",
                "Satuan": "satuan",
                "Kapasitas-produk": "kapasitas_produk",
                "Bahan_baku_aktif": "bahan_baku_aktif",
                "Bahan_baku": "bahan_baku",
                "jumlah_bahan_baku": "jumlah_bahan_baku",
                "Periode_produksi": "periode_produksi",
                "Stok": "stok",
                "status_data": "status_data",
                "satuan_bahan_baku": "satuan_bahan_baku",
                "nilai_bahan_baku": "nilai_bahan_baku",
                "satuan_stok": "satuan_stok",
                "nilai_stok": "nilai_stok",
            },
        )

        # 8. PENJUALAN
        import_csv(
            session,
            "Data_Penjualan.csv",
            Penjualan,
            column_mapping={
                "Bulan": "bulan",
                "Produk": "nama_produk",
                "Jumlah_Terjual": "jumlah_terjual",
                "Harga_Satuan": "harga_satuan",
                "Total_Penjualan": "total_penjualan",
                "Satuan": "satuan",
                "Kanal": "kanal",
                "Status_Data": "status_data",
            },
            date_columns=["bulan"],
        )

        print("\n" + "=" * 55)
        print("IMPORT SELURUH DATA BERHASIL!")
        print("=" * 55)

    except Exception as error:
        session.rollback()
        print("\nIMPORT DATA GAGAL!")
        print("Penyebab:", error)
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
