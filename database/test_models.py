print("TEST MODELS BERJALAN!")

from database.models import Base

print("Model berhasil diimpor!")
print("\nDaftar tabel:")

for table_name, table in Base.metadata.tables.items():
    print(f"\nTabel: {table_name}")
    for column in table.columns:
        print(f" - {column.name}: {column.type}")