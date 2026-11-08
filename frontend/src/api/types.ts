// ============================================================
// VINIX7 — API types (mirror FastAPI response contracts)
// ============================================================

export interface DashboardSummary {
  total_bahan_organik: number
  total_produk: number
  total_data_produksi: number
  total_data_penjualan: number
  total_data_prediksi: number
  total_prediksi_penjualan_2026: number
}

export interface OrganicAnalysis {
  bahan_id: string
  jenis_bahan_organik: string
  kategori_bahan: string | null
  jumlah_ketersediaan: number | null
  satuan: string | null
  kontinuitas: string | null
  jarak_ke_produksi_km: number | null
  kemudahan_pengumpulan: string | null
}

export interface OrganicRanking {
  peringkat: number
  jenis_bahan_organik: string
  skor_akhir: number
}

export interface PredictionEntry {
  id: number
  bulan: string // ISO date string
  produk: string
  prediksi_penjualan: number
  model: string
  tanggal_prediksi: string
}

export interface PredictionSummary {
  produk: string
  total_prediksi: number
}

export interface Product {
  produk_id: string
  nama_produk: string
  jenis_produk: string | null
  deskripsi: string | null
  manfaat: string | null
  harga: string | number | null // Numeric serializes as string
  ukuran_kemasan: string | null
  produsen: string | null
  lokasi_produsen: string | null
  kontak: string | null
  stok_ketersediaan: string | null
  foto_produk: string | null
}