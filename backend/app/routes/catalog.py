
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db

from backend.app.services.catalog_service import (
    get_all_products,
    get_product_by_id
)

from backend.app.schemas.produk import ProdukResponse


router = APIRouter(
    prefix="/catalog",
    tags=["Katalog Produk"]
)


@router.get(
    "/products",
    response_model=list[ProdukResponse]
)
def catalog_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get(
    "/products/{produk_id}",
    response_model=ProdukResponse
)
def catalog_product_detail(
    produk_id: str,
    db: Session = Depends(get_db)
):
    produk = get_product_by_id(db, produk_id)

    if produk is None:
        raise HTTPException(
            status_code=404,
            detail="Produk tidak ditemukan"
        )

    return produk
