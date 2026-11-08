
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.services.dashboard_service import get_dashboard_summary


def test_dashboard_service():
    with Session(engine) as db:
        hasil = get_dashboard_summary(db)

        print("\n=== HASIL DASHBOARD SERVICE VINIX7 ===")

        for nama, nilai in hasil.items():
            print(f"{nama}: {nilai}")


if __name__ == "__main__":
    test_dashboard_service()