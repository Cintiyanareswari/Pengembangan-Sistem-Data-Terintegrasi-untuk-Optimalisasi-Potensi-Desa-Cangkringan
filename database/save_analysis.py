
import pandas as pd
from pathlib import Path
from database.connection import engine

DATA_DIR = Path("storage/analysis")


def simpan_ke_database(nama_file, nama_tabel):
    file_path = DATA_DIR / nama_file

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}"
        )

    df = pd.read_csv(file_path)

    df.to_sql(
        name=nama_tabel,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        f"{nama_file} berhasil disimpan "
        f"ke tabel {nama_tabel} ({len(df)} baris)."
    )


def main():
    print("PENYIMPANAN HASIL ANALISIS KE POSTGRESQL")
    print("=" * 45)

    simpan_ke_database(
        "analisis_organik.csv",
        "hasil_analisis_organik"
    )

    simpan_ke_database(
        "bobot_ahp.csv",
        "bobot_ahp"
    )

    simpan_ke_database(
        "hasil_scoring_organik.csv",
        "hasil_scoring_organik"
    )

    print("=" * 45)
    print("SEMUA HASIL ANALISIS BERHASIL DISIMPAN!")


if __name__ == "__main__":
    main()
