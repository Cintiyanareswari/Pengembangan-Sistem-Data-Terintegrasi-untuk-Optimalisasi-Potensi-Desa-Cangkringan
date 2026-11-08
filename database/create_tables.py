
from database.models import Base
from database.connection import engine

def create_tables():
    try:
        print("Memulai pembuatan tabel...")

        Base.metadata.create_all(bind=engine)

        print("Tabel berhasil dibuat!")

        print("\nDaftar tabel yang terdaftar:")
        for table_name in Base.metadata.tables:
            print("-", table_name)

    except Exception as e:
        print("Gagal membuat tabel!")
        print("Detail error:", e)
        raise


if __name__ == "__main__":
    create_tables()
