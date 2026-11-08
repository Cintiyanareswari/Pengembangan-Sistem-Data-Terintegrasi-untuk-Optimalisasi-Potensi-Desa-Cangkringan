
from sqlalchemy.orm import Session

from database.models import Produk


def get_all_products(db: Session):
    """
    Mengambil seluruh data produk dari PostgreSQL.
    """
    return (
        db.query(Produk)
        .order_by(Produk.nama_produk.asc())
        .all()
    )


def get_product_by_id(db: Session, produk_id: str):
    """
    Mengambil detail produk berdasarkan ID produk.
    """
    return (
        db.query(Produk)
        .filter(Produk.produk_id == produk_id)
        .first()
    )
