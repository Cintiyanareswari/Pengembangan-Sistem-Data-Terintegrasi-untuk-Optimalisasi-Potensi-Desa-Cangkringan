
from pathlib import Path
import pandas as pd

from sqlalchemy.orm import Session
from database.connection import engine
from database.models import PrediksiPenjualan


def save_prediction():
    # Lokasi file CSV
    root_dir = Path(__file__).resolve().parents[3]
    csv_path = root_dir / "storage" / "machine_learning" / "hasil_prediksi_2026.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {csv_path}")

    # Membaca data prediksi
    df = pd.read_csv(csv_path)

    # Validasi kolom
    required_columns = ["Bulan", "Produk", "Prediksi_Penjualan"]

    if not all(col in df.columns for col in required_columns):
        raise ValueError("Kolom CSV tidak sesuai dengan format yang dibutuhkan.")

    # Membersihkan dan menyesuaikan tipe data
    df["Bulan"] = pd.to_datetime(df["Bulan"]).dt.date
    df["Produk"] = df["Produk"].astype(str).str.strip()
    df["Prediksi_Penjualan"] = pd.to_numeric(
        df["Prediksi_Penjualan"], errors="raise"
    )

    if df[required_columns].isnull().any().any():
        raise ValueError("CSV memiliki data kosong.")

    if df.duplicated(subset=["Bulan", "Produk"]).any():
        raise ValueError("Terdapat prediksi ganda untuk bulan dan produk yang sama.")

    # Simpan ke PostgreSQL
    with Session(engine) as session:
        try:
            # Hapus prediksi tahun 2026 sebelumnya agar tidak duplikat
            session.query(PrediksiPenjualan).filter(
                PrediksiPenjualan.bulan >= pd.Timestamp("2026-01-01").date(),
                PrediksiPenjualan.bulan < pd.Timestamp("2027-01-01").date()
            ).delete(synchronize_session=False)

            for _, row in df.iterrows():
                data = PrediksiPenjualan(
                    bulan=row["Bulan"],
                    produk=row["Produk"],
                    prediksi_penjualan=float(row["Prediksi_Penjualan"]),
                    model="Extra Trees Regressor",
                    tanggal_prediksi=pd.Timestamp.today().date()
                )
                session.add(data)

            session.commit()

            print("Berhasil menyimpan hasil prediksi!")
            print(f"Jumlah data CSV       : {len(df)}")
            print("Jumlah data tersimpan : 132")
            print("Periode prediksi      : Januari - Desember 2026")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    save_prediction()
