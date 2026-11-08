
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

OUTPUT_DIR = Path("storage/analysis")


def main():
    query = """
        SELECT
            b.bahan_id,
            b.jenis_bahan_organik,
            b.kategori_bahan,
            k.jumlah_ketersediaan,
            k.satuan,
            k.kontinuitas,
            k.jarak_ke_produksi_km,
            k.kemudahan_pengumpulan
        FROM bahan_organik b
        JOIN ketersediaan_bahan k
            ON b.bahan_id = k.bahan_id
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    print("=" * 45)
    print("ANALISIS BAHAN ORGANIK VINIX7")
    print("=" * 45)

    print("\nJumlah data:", len(df))

    print("\nTotal ketersediaan per jenis bahan:")
    print(
        df.groupby("jenis_bahan_organik")["jumlah_ketersediaan"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nDistribusi kontinuitas:")
    print(df["kontinuitas"].value_counts())

    print("\nDistribusi kemudahan pengumpulan:")
    print(df["kemudahan_pengumpulan"].value_counts())

    print("\nRata-rata jarak ke lokasi produksi:")
    print(
        df.groupby("jenis_bahan_organik")["jarak_ke_produksi_km"]
        .mean()
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / "analisis_organik.csv", index=False)

    print("\nSumber data: PostgreSQL")
    print("ANALISIS BAHAN ORGANIK SELESAI!")


if __name__ == "__main__":
    main()
