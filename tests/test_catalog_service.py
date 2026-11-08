
from sqlalchemy.orm import Session

from database.connection import engine
from backend.app.services.catalog_service import (
    get_all_products,
    get_product_by_id
)


def test_catalog_service():
    with Session(engine) as db:

        # 1. Menguji pengambilan seluruh produk
        products = get_all_products(db)

        print("\n=== PENGUJIAN CATALOG SERVICE ===")
        print(f"Total produk: {len(products)}")

        # Memastikan jumlah produk sesuai database
        assert len(products) == 11, (
            f"Jumlah produk tidak sesuai: {len(products)}"
        )

        # Memastikan setiap produk memiliki ID dan nama
        for produk in products:
            assert produk.produk_id is not None
            assert produk.nama_produk is not None

            print(
                f"{produk.produk_id} - {produk.nama_produk}"
            )

        # 2. Menguji pengambilan detail produk
        produk_pertama = products[0]

        detail = get_product_by_id(
            db,
            produk_pertama.produk_id
        )

        assert detail is not None
        assert detail.produk_id == produk_pertama.produk_id

        print("\n=== DETAIL PRODUK ===")
        print(f"ID: {detail.produk_id}")
        print(f"Nama: {detail.nama_produk}")

        # 3. Menguji ID yang tidak ditemukan
        produk_tidak_ada = get_product_by_id(
            db,
            "ID-PRODUK-TIDAK-ADA"
        )

        assert produk_tidak_ada is None

        print("\nPengujian catalog service berhasil!")


if __name__ == "__main__":
    test_catalog_service()
