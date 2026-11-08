
from sqlalchemy import text
from database.connection import engine

print("Memulai pengujian koneksi PostgreSQL...")

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Koneksi PostgreSQL berhasil!")
        print("Hasil pengujian:", result.scalar())

except Exception as e:
    print("Koneksi PostgreSQL gagal!")
    print("Detail error:", e)
