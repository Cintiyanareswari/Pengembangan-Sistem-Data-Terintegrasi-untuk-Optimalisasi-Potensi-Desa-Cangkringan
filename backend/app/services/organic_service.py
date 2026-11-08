
from sqlalchemy import text
from sqlalchemy.orm import Session


def get_analisis_organik(db: Session):
    query = text("""
        SELECT
            bahan_id,
            jenis_bahan_organik,
            kategori_bahan,
            jumlah_ketersediaan,
            satuan,
            kontinuitas,
            jarak_ke_produksi_km,
            kemudahan_pengumpulan
        FROM hasil_analisis_organik
        ORDER BY jenis_bahan_organik
    """)

    result = db.execute(query).mappings().all()

    return [dict(row) for row in result]


def get_ranking_organik(db: Session):
    query = text("""
        SELECT
            ROW_NUMBER() OVER (
                ORDER BY skor_akhir DESC
            ) AS peringkat,
            jenis_bahan_organik,
            skor_akhir
        FROM hasil_scoring_organik
        ORDER BY skor_akhir DESC
    """)

    result = db.execute(query).mappings().all()

    return [dict(row) for row in result]


def get_organic_summary(db: Session):
    return {
        "analisis_organik": get_analisis_organik(db),
        "ranking_organik": get_ranking_organik(db)
    }
