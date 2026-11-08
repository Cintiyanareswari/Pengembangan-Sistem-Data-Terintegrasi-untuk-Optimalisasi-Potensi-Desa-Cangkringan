
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.routes.organic import (
    organic_analysis,
    organic_ranking
)


def test_organic_route():
    with Session(engine) as db:

        # 1. Menguji endpoint analisis organik
        hasil_analisis = organic_analysis(db)

        print("\n=== HASIL ORGANIC ANALYSIS ===")
        print(f"Total data analisis: {len(hasil_analisis)}")

        assert len(hasil_analisis) > 0

        for data in hasil_analisis[:5]:
            print(data)

        # 2. Menguji endpoint ranking organik
        hasil_ranking = organic_ranking(db)

        print("\n=== HASIL ORGANIC RANKING ===")
        print(f"Total ranking: {len(hasil_ranking)}")

        assert len(hasil_ranking) == 17

        # Memastikan urutan ranking benar
        assert hasil_ranking[0]["peringkat"] == 1
        assert hasil_ranking[0]["jenis_bahan_organik"] == (
            "Bahan fermentasi organik"
        )

        for data in hasil_ranking[:5]:
            print(
                f"Peringkat {data['peringkat']}: "
                f"{data['jenis_bahan_organik']} - "
                f"{data['skor_akhir']}"
            )

        print("\nPengujian organic route berhasil!")


if __name__ == "__main__":
    test_organic_route()
