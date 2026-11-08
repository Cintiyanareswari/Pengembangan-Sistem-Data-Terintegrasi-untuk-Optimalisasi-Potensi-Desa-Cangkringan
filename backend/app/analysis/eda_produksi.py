
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

OUTPUT_DIR = Path("storage/analysis")


def main():
    query = """
        SELECT *
        FROM produksi
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    print("=" * 40)
    print("EDA DATA PRODUKSI VINIX7")
    print("=" * 40)

    print("\nJumlah data produksi:", len(df))

    print("\nJumlah produksi per produk:")
    hasil = (
        df.groupby("Nama_Produk")["Jumlah_produksi_total"]
        .sum()
        .sort_values(ascending=False)
    )
    print(hasil)

    print("\nStatistik jumlah produksi:")
    print(df["Jumlah_produksi_total"].describe())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    hasil.to_csv(OUTPUT_DIR / "hasil_eda_produksi.csv")

    print("\nSumber data: PostgreSQL - tabel produksi")
    print("EDA PRODUKSI SELESAI!")


if __name__ == "__main__":
    main()
