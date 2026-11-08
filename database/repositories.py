
from sqlalchemy.orm import Session


class BaseRepository:
    """
    Repository dasar untuk operasi CRUD.
    Setiap repository menggunakan model SQLAlchemy.
    """

    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def create(self, data):
        try:
            record = self.model(**data)
            self.session.add(record)
            self.session.commit()
            self.session.refresh(record)
            return record
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, record_id):
        return self.session.get(self.model, record_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, record_id, data):
        try:
            record = self.get_by_id(record_id)

            if record is None:
                return None

            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            self.session.commit()
            self.session.refresh(record)
            return record

        except Exception:
            self.session.rollback()
            raise

    def delete(self, record_id):
        try:
            record = self.get_by_id(record_id)

            if record is None:
                return False

            self.session.delete(record)
            self.session.commit()
            return True

        except Exception:
            self.session.rollback()
            raise


# Repository khusus setiap model

from database.models import (
    Kalurahan,
    Padukuhan,
    Pertanian,
    BahanOrganik,
    KetersediaanBahan,
    Produk,
    Produksi,
    Penjualan,
)


class KalurahanRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Kalurahan)


class PadukuhanRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Padukuhan)


class PertanianRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Pertanian)


class BahanOrganikRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, BahanOrganik)


class KetersediaanBahanRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, KetersediaanBahan)


class ProdukRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Produk)


class ProduksiRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Produksi)


class PenjualanRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Penjualan)
