import { useEffect, useMemo, useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { LoadingState, ErrorState, EmptyState } from '../components/States'
import { ProductCard } from '../features/catalog/ProductCard'
import { ProductDetailDialog } from '../features/catalog/ProductDetailDialog'

export function KatalogPage() {
  const { data, loading, error, refetch } = useFetch(() => api.getProducts())
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    document.title = 'AKAR TANI · Katalog Produk'
  }, [])

  const rows = useMemo(() => {
    if (!data) return []
    const q = query.trim().toLowerCase()
    if (!q) return data
    return data.filter(
      (p) =>
        p.nama_produk.toLowerCase().includes(q) ||
        (p.jenis_produk ?? '').toLowerCase().includes(q) ||
        (p.deskripsi ?? '').toLowerCase().includes(q),
    )
  }, [data, query])

  return (
    <div className="page">
      <Card>
        <CardHeader
          title="Katalog Produk"
          subtitle="Pupuk dan probiotik produksi desa"
        />
        <div className="toolbar">
          <input
            type="search"
            className="input"
            placeholder="Cari produk…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Cari produk"
          />
          <span className="toolbar__count tnum">{rows.length} produk</span>
        </div>

        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState detail={error} onRetry={refetch} />
        ) : rows.length === 0 ? (
          <EmptyState
            title="Produk tidak ditemukan"
            detail={query ? 'Coba kata kunci lain.' : 'Belum ada produk.'}
          />
        ) : (
          <div className="pcards pcards--grid">
            {rows.map((p) => (
              <ProductCard
                key={p.produk_id}
                product={p}
                onOpen={setSelectedId}
              />
            ))}
          </div>
        )}
      </Card>

      {selectedId && (
        <ProductDetailDialog
          produkId={selectedId}
          onClose={() => setSelectedId(null)}
        />
      )}
    </div>
  )
}