
from sqlalchemy.orm import Session

from database.connection import engine

from backend.app.routes.catalog import (
    catalog_products,
    catalog_product_detail
)


def test_catalog_route():
    with Session(engine) as db:

        # 1. Menguji pengambilan seluruh produk
        hasil_produk = catalog_products(db)

        print("\n=== HASIL CATALOG PRODUCTS ===")
        print(f"Total produk: {len(hasil_produk)}")

        # Memastikan terdapat 11 produk
        assert len(hasil_produk) == 11

        for produk in hasil_produk:
            assert produk.produk_id is not None
            assert produk.nama_produk is not None

            print(
                f"{produk.produk_id} - {produk.nama_produk}"
            )

        # 2. Menguji detail produk
        produk_pertama = hasil_produk[0]

        detail = catalog_product_detail(
            produk_pertama.produk_id,
            db
        )

        print("\n=== DETAIL PRODUK ===")
        print(f"ID: {detail.produk_id}")
        print(f"Nama: {detail.nama_produk}")

        assert detail is not None
        assert detail.produk_id == produk_pertama.produk_id

        # 3. Menguji produk yang tidak ditemukan
        from fastapi import HTTPException

        try:
            catalog_product_detail(
                "ID-PRODUK-TIDAK-ADA",
                db
            )
            assert False, "Seharusnya menghasilkan HTTP 404"

        except HTTPException as error:
            assert error.status_code == 404
            print("\nProduk tidak ditemukan: HTTP 404")

        print("\nPengujian catalog route berhasil!")


if __name__ == "__main__":
    test_catalog_route()
