
import pandas as pd

from backend.app.data_engineering.load_data import (
    load_raw_data,
    SHEET_NAMES
)


def test_load_raw_data():

    print("\n=== PENGUJIAN DATA LOADING VINIX7 ===")

    # Memuat dataset Excel
    data = load_raw_data()

    # 1. Memastikan hasil berupa dictionary
    assert isinstance(data, dict), (
        "Hasil loading harus berupa dictionary"
    )

    # 2. Memastikan seluruh sheet berhasil dimuat
    assert set(data.keys()) == set(SHEET_NAMES), (
        "Sheet yang dimuat tidak sesuai"
    )

    # 3. Memastikan setiap sheet berbentuk DataFrame
    for nama_sheet, df in data.items():

        assert isinstance(df, pd.DataFrame), (
            f"{nama_sheet} bukan DataFrame"
        )

        assert len(df.columns) > 0, (
            f"{nama_sheet} tidak memiliki kolom"
        )

        print(
            f"{nama_sheet}: "
            f"{len(df)} baris, "
            f"{len(df.columns)} kolom"
        )

    print("\nPengujian data loading berhasil!")


if __name__ == "__main__":
    test_load_raw_data()
