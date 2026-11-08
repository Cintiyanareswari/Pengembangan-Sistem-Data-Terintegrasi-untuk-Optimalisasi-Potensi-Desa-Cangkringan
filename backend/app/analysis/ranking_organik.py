
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

OUTPUT_DIR = Path("storage/analysis")


def main():
    print("=" * 45)
    print("RANKING POTENSI BAHAN ORGANIK")
    print("=" * 45)

    # 1. Mengambil hasil scoring dari PostgreSQL
    query = """
        SELECT jenis_bahan_organik, skor_akhir
        FROM hasil_scoring_organik
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    if df.empty:
        raise ValueError("Data scoring bahan organik kosong.")

    # 2. Mengurutkan skor dari tertinggi ke terendah
    ranking = df.sort_values(
        by="skor_akhir",
        ascending=False
    ).reset_index(drop=True)

    # 3. Menambahkan nomor peringkat
    ranking.insert(
        0,
        "peringkat",
        range(1, len(ranking) + 1)
    )

    # 4. Menyimpan hasil ke CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ranking.to_csv(
        OUTPUT_DIR / "ranking_organik.csv",
        index=False
    )

    # 5. Menyimpan hasil ke PostgreSQL
    ranking.to_sql(
        name="ranking_organik",
        con=engine,
        if_exists="replace",
        index=False
    )

    # 6. Menampilkan hasil ranking
    print("\nHASIL RANKING BAHAN ORGANIK:\n")
    print(ranking.to_string(index=False))

    print("\nJumlah jenis bahan:", len(ranking))
    print("Hasil CSV: storage/analysis/ranking_organik.csv")
    print("Hasil PostgreSQL: tabel ranking_organik")
    print("\nRANKING ORGANIK SELESAI!")


if __name__ == "__main__":
    main()
