
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Numeric,
    Date,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship


# =====================================================
# BASE MODEL
# =====================================================

Base = declarative_base()


# =====================================================
# 1. KALURAHAN
# Sumber: Data_Wilayah_Kalurahan.csv (5 baris)
# =====================================================

class Kalurahan(Base):
    __tablename__ = "kalurahan"

    kalurahan_id = Column(String(30), primary_key=True)
    kalurahan = Column(String(150), nullable=False)

    luas_kalurahan_ha = Column(Float)
    jumlah_padukuhan = Column(Integer)
    jumlah_rw = Column(Integer)
    jumlah_rt = Column(Integer)

    batas_utara = Column(Text)
    batas_selatan = Column(Text)
    batas_barat = Column(Text)
    batas_timur = Column(Text)

    jarak_kecamatan_km = Column(Float)
    jarak_kabupaten_km = Column(Float)
    jarak_provinsi_km = Column(Float)
    jarak_nasional_km = Column(Float)

    latitude = Column(Float)
    longitude = Column(Float)

    padukuhan = relationship(
        "Padukuhan",
        back_populates="kalurahan_ref"
    )


# =====================================================
# 2. PADUKUHAN
# Sumber: Data_Wilayah_Padukuhan.csv (73 baris)
# =====================================================

class Padukuhan(Base):
    __tablename__ = "padukuhan"

    padukuhan_id = Column(String(30), primary_key=True)

    kalurahan_id = Column(
        String(30),
        ForeignKey("kalurahan.kalurahan_id"),
        nullable=False
    )

    kalurahan = Column(String(150))
    nama_padukuhan = Column(
        "padukuhan",
        String(150),
        nullable=False
    )

    jumlah_rt = Column(Integer)
    jumlah_rw = Column(Integer)

    latitude = Column(Float)
    longitude = Column(Float)

    kalurahan_ref = relationship(
        "Kalurahan",
        back_populates="padukuhan"
    )

    pertanian = relationship(
        "Pertanian",
        back_populates="padukuhan_ref"
    )

    ketersediaan_bahan = relationship(
        "KetersediaanBahan",
        back_populates="padukuhan_ref"
    )


# =====================================================
# 3. PERTANIAN
# Sumber: Data_Pertanian.csv (511 baris)
# =====================================================

class Pertanian(Base):
    __tablename__ = "pertanian"

    agri_id = Column(String(30), primary_key=True)

    kalurahan = Column(String(150))

    padukuhan_id = Column(
        String(30),
        ForeignKey("padukuhan.padukuhan_id"),
        nullable=False
    )

    nama_padukuhan = Column(
        "padukuhan",
        String(150)
    )

    komoditas = Column(String(150))
    kelompok_komoditas = Column(String(150))

    tahun = Column(Integer)

    luas_panen_ha = Column(Float)
    luas_lahan_ha = Column(Float)

    jumlah_petani = Column(Integer)
    jumlah_utp = Column(Integer)
    jumlah_kelompok_tani = Column(Integer)

    produksi = Column(Float)
    satuan_produksi_q = Column(String(50))

    padukuhan_ref = relationship(
        "Padukuhan",
        back_populates="pertanian"
    )


# =====================================================
# 4. BAHAN ORGANIK
# Sumber: Data_Bahan_Organik.csv
# 17 bahan unik
# =====================================================

class BahanOrganik(Base):
    __tablename__ = "bahan_organik"

    bahan_id = Column(String(30), primary_key=True)

    jenis_bahan_organik = Column(
        String(200),
        nullable=False
    )

    kategori_bahan = Column(String(150))

    ketersediaan = relationship(
        "KetersediaanBahan",
        back_populates="bahan_ref"
    )


# =====================================================
# 5. KETERSEDIAAN BAHAN
# Sumber: Data_Bahan_Organik.csv
# 88 catatan ketersediaan
# =====================================================

class KetersediaanBahan(Base):
    __tablename__ = "ketersediaan_bahan"

    ketersediaan_id = Column(
        String(30),
        primary_key=True
    )

    bahan_id = Column(
        String(30),
        ForeignKey("bahan_organik.bahan_id"),
        nullable=False
    )

    padukuhan_id = Column(
        String(30),
        ForeignKey("padukuhan.padukuhan_id"),
        nullable=False
    )

    periode = Column(Date)

    jumlah_ketersediaan = Column(Float)
    satuan = Column(String(50))

    kontinuitas = Column(String(150))
    jarak_ke_produksi_km = Column(Float)

    kemudahan_pengumpulan = Column(String(150))
    status_pemanfaatan = Column(String(150))

    frekuensi = Column(String(150))
    musim = Column(String(150))

    jumlah_sumber = Column(Integer)
    status_data = Column(String(100))

    bahan_ref = relationship(
        "BahanOrganik",
        back_populates="ketersediaan"
    )

    padukuhan_ref = relationship(
        "Padukuhan",
        back_populates="ketersediaan_bahan"
    )


# =====================================================
# 6. PRODUK
# Sumber: Data_Produk_Katalog.csv (11 baris)
# =====================================================

class Produk(Base):
    __tablename__ = "produk"

    produk_id = Column(String(30), primary_key=True)

    nama_produk = Column(
        "Nama_Produk",
        String(200),
        nullable=False
    )

    jenis_produk = Column(
        "Jenis_Produk",
        String(150)
    )

    deskripsi = Column("Deskripsi", Text)
    manfaat = Column("Manfaat", Text)

    harga = Column(
        "Harga",
        Numeric(18, 2)
    )

    ukuran_kemasan = Column(
        "Ukuran_Kemasan",
        String(100)
    )

    produsen = Column("Produsen", String(200))

    lokasi_produsen = Column(
        "Lokasi_Produsen",
        String(200)
    )

    kontak = Column("Kontak", String(100))

    stok_ketersediaan = Column(
        "Stok_Ketersediaan",
        String(100)
    )

    foto_produk = Column(
        "Foto Produk",
        Text
    )

    produksi = relationship(
        "Produksi",
        back_populates="produk_ref"
    )

    penjualan = relationship(
        "Penjualan",
        back_populates="produk_ref"
    )


# =====================================================
# 7. PRODUKSI
# Sumber: Data_produksi_pupuk.csv (66 baris)
# =====================================================

class Produksi(Base):
    __tablename__ = "produksi"

    produksi_id = Column(String(30), primary_key=True)

    produk_id = Column(
        String(30),
        ForeignKey("produk.produk_id"),
        nullable=False
    )

    nama_produk = Column(
        "Nama_Produk",
        String(200)
    )

    jenis_produk = Column(
        "Jenis_Produk",
        String(150)
    )

    jumlah_produksi_varian = Column(
        "Jumlah_produksi_varian",
        Integer
    )

    jumlah_produksi_total = Column(
        "Jumlah_produksi_total",
        Integer
    )

    satuan = Column("Satuan", String(50))

    kapasitas_produk = Column(
        "Kapasitas-produk",
        Integer
    )

    bahan_baku_aktif = Column(
        "Bahan_baku_aktif",
        Text
    )

    bahan_baku = Column(
        "Bahan_baku",
        Text
    )

    jumlah_bahan_baku = Column(
        "jumlah_bahan_baku",
        String(100)
    )

    periode_produksi = Column(
        "Periode_produksi",
        Integer
    )

    stok = Column("Stok", String(100))

    status_data = Column(
        "status_data",
        String(100)
    )

    satuan_bahan_baku = Column(String(50))
    nilai_bahan_baku = Column(Integer)

    satuan_stok = Column(String(50))
    nilai_stok = Column(Integer)

    produk_ref = relationship(
        "Produk",
        back_populates="produksi"
    )


# =====================================================
# 8. PENJUALAN
# Sumber: Data_Penjualan.csv (792 baris)
# =====================================================

class Penjualan(Base):
    __tablename__ = "penjualan"

    Penjualan_id = Column(
        String(30),
        primary_key=True
    )

    Produk_id = Column(
        String(30),
        ForeignKey("produk.produk_id"),
        nullable=False
    )

    bulan = Column("Bulan", Date)

    nama_produk = Column(
        "Produk",
        String(200)
    )

    jumlah_terjual = Column(
        "Jumlah_Terjual",
        Integer
    )

    harga_satuan = Column(
        "Harga_Satuan",
        Numeric(18, 2)
    )

    total_penjualan = Column(
        "Total_Penjualan",
        Numeric(18, 2)
    )

    satuan = Column("Satuan", String(50))
    kanal = Column("Kanal", String(100))

    status_data = Column(
        "Status_Data",
        String(100)
    )

    produk_ref = relationship(
        "Produk",
        back_populates="penjualan"
    )


# =====================================================
# 9. PREDIKSI PENJUALAN
# Sumber: hasil_prediksi_2026.csv
# =====================================================

class PrediksiPenjualan(Base):
    __tablename__ = "prediksi_penjualan"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    bulan = Column(
        "bulan",
        Date,
        nullable=False
    )

    produk = Column(
        "produk",
        String(200),
        nullable=False
    )

    prediksi_penjualan = Column(
        "prediksi_penjualan",
        Float,
        nullable=False
    )

    model = Column(
        "model",
        String(100),
        nullable=False
    )

    tanggal_prediksi = Column(
        "tanggal_prediksi",
        Date,
        nullable=False
    )