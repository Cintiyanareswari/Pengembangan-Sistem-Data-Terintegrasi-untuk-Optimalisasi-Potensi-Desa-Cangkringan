
from backend.app.schemas.bahan_organik import (
    BahanOrganikCreate,
    BahanOrganikResponse,
)
from backend.app.schemas.ketersediaan_bahan import (
    KetersediaanBahanCreate,
    KetersediaanBahanResponse,
)
from backend.app.schemas.produk import ProdukCreate, ProdukResponse
from backend.app.schemas.produksi import ProduksiCreate, ProduksiResponse
from backend.app.schemas.penjualan import PenjualanCreate, PenjualanResponse
from backend.app.schemas.prediksi_penjualan import (
    PrediksiPenjualanCreate,
    PrediksiPenjualanResponse,
)
from backend.app.schemas.analisis_organik import AnalisisOrganikResponse
from backend.app.schemas.ranking_organik import RankingOrganikResponse


def test_schema_import():
    print("Semua schema berhasil diimpor!")


if __name__ == "__main__":
    test_schema_import()