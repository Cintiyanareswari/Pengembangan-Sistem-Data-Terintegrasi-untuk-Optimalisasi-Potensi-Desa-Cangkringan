
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

OUTPUT_DIR = Path("storage/analysis")


def main():
    query = """
        SELECT *
        FROM penjualan
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    print("=" * 40)
    print("EDA DATA PENJUALAN VINIX7")
    print("=" * 40)

    print("\nJumlah data penjualan:", len(df))

    print("\nTotal penjualan per produk:")
    hasil = (
        df.groupby("Produk")["Jumlah_Terjual"]
        .sum()
        .sort_values(ascending=False)
    )
    print(hasil)

    print("\nStatistik jumlah produk terjual:")
    print(df["Jumlah_Terjual"].describe())

    print("\nTotal penjualan berdasarkan bulan:")
    df["Bulan"] = pd.to_datetime(df["Bulan"], errors="coerce")
    bulanan = df.groupby(df["Bulan"].dt.to_period("M"))["Total_Penjualan"].sum()
    print(bulanan)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    hasil.to_csv(OUTPUT_DIR / "hasil_eda_penjualan.csv")

    print("\nSumber data: PostgreSQL - tabel penjualan")
    print("EDA PENJUALAN SELESAI!")


if __name__ == "__main__":
    main()
