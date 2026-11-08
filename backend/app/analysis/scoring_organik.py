
import pandas as pd
from sqlalchemy import text
from database.connection import engine
from pathlib import Path

DATA_DIR = Path("storage/analysis")
BOBOT_PATH = DATA_DIR / "bobot_ahp.csv"


def main():
    # 1. Mengambil data dari PostgreSQL
    query = """
        SELECT
            b.jenis_bahan_organik,
            k.jumlah_ketersediaan,
            k.kontinuitas,
            k.jarak_ke_produksi_km,
            k.kemudahan_pengumpulan,
            k.satuan
        FROM bahan_organik b
        JOIN ketersediaan_bahan k
            ON b.bahan_id = k.bahan_id
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    # 2. Memastikan satuan ketersediaan sama
    satuan = df["satuan"].dropna().str.lower().unique()

    if len(satuan) != 1 or satuan[0] != "kg":
        raise ValueError("Satuan ketersediaan harus seragam dalam kg.")

    # 3. Mengubah kategori menjadi nilai numerik
    kontinuitas_map = {
        "Kontinu": 4,
        "Cukup kontinu": 3,
        "Musiman": 2,
        "Tidak kontinu": 1
    }

    kemudahan_map = {
        "Mudah": 3,
        "Sedang": 2,
        "Sulit": 1
    }

    df["skor_kontinuitas"] = df["kontinuitas"].map(kontinuitas_map)
    df["skor_kemudahan"] = df["kemudahan_pengumpulan"].map(kemudahan_map)

    if df[["skor_kontinuitas", "skor_kemudahan"]].isna().any().any():
        raise ValueError("Ada kategori yang belum memiliki nilai penilaian.")

    # 4. Agregasi berdasarkan jenis bahan
    data = df.groupby("jenis_bahan_organik").agg(
        ketersediaan=("jumlah_ketersediaan", "mean"),
        kontinuitas=("skor_kontinuitas", "mean"),
        jarak=("jarak_ke_produksi_km", "mean"),
        kemudahan=("skor_kemudahan", "mean")
    ).reset_index()

    # 5. Normalisasi SAW
    # Benefit: semakin besar semakin baik
    data["norm_ketersediaan"] = (
        data["ketersediaan"] / data["ketersediaan"].max()
    )

    data["norm_kontinuitas"] = (
        data["kontinuitas"] / data["kontinuitas"].max()
    )

    data["norm_kemudahan"] = (
        data["kemudahan"] / data["kemudahan"].max()
    )

    # Cost: semakin kecil semakin baik
    data["norm_jarak"] = (
        data["jarak"].min() / data["jarak"]
    )

    # 6. Membaca bobot hasil AHP
    bobot_df = pd.read_csv(BOBOT_PATH)
    bobot = dict(zip(bobot_df["kriteria"], bobot_df["bobot"]))

    kriteria = ["ketersediaan", "kontinuitas", "jarak", "kemudahan"]

    if set(bobot.keys()) != set(kriteria):
        raise ValueError("Kriteria pada bobot AHP tidak sesuai.")

    if abs(sum(bobot.values()) - 1) > 0.001:
        raise ValueError("Total bobot AHP harus sama dengan 1.")

    # 7. Menghitung skor akhir SAW
    data["skor_akhir"] = (
        data["norm_ketersediaan"] * bobot["ketersediaan"]
        + data["norm_kontinuitas"] * bobot["kontinuitas"]
        + data["norm_jarak"] * bobot["jarak"]
        + data["norm_kemudahan"] * bobot["kemudahan"]
    )

    # 8. Menyimpan hasil scoring
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data.to_csv(
        DATA_DIR / "hasil_scoring_organik.csv",
        index=False
    )

    print("=" * 45)
    print("SCORING BAHAN ORGANIK METODE AHP-SAW")
    print("=" * 45)

    print("\nBobot AHP yang digunakan:")
    print(bobot_df.to_string(index=False))

    print("\nHasil scoring SAW:")
    print(
        data[["jenis_bahan_organik", "skor_akhir"]]
        .sort_values("skor_akhir", ascending=False)
        .to_string(index=False)
    )

    print("\nJumlah jenis bahan:", len(data))
    print("Sumber data: PostgreSQL")
    print("Bobot: hasil pembobotan AHP")
    print("Hasil tersimpan di storage/analysis/hasil_scoring_organik.csv")
    print("SCORING ORGANIK SELESAI!")


if __name__ == "__main__":
    main()
