
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.services.organic_service import (
    get_analisis_organik,
    get_ranking_organik,
    get_organic_summary,
)


def test_organic_service():
    with Session(engine) as db:
        hasil = get_organic_summary(db)

        analisis = hasil["analisis_organik"]
        ranking = hasil["ranking_organik"]

        print("\n=== HASIL ORGANIC SERVICE VINIX7 ===")

        print("Jumlah data analisis organik:", len(analisis))
        print("Jumlah ranking organik:", len(ranking))

        print("\n=== TOP 5 RANKING ORGANIK ===")
        for item in ranking[:5]:
            print(item)


if __name__ == "__main__":
    test_organic_service()