
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.services.prediction_service import (
    get_prediction_2026,
    get_prediction_summary,
)


def test_prediction_service():
    with Session(engine) as db:
        data_prediksi = get_prediction_2026(db)
        ringkasan = get_prediction_summary(db)

        print("\n=== HASIL PREDICTION SERVICE VINIX7 ===")

        print("Jumlah data prediksi:", len(data_prediksi))

        print("\n=== RINGKASAN PREDIKSI PER PRODUK ===")
        for item in ringkasan:
            print(item)


if __name__ == "__main__":
    test_prediction_service()