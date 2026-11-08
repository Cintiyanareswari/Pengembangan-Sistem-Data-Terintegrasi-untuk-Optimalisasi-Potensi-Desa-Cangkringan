import { useEffect, useMemo, useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { LoadingState, ErrorState, EmptyState } from '../components/States'
import { formatNumber } from '../utils/format'

export function BahanOrganikPage() {
  const { data, loading, error, refetch } = useFetch(() =>
    api.getOrganicAnalysis(),
  )
  const [query, setQuery] = useState('')

  useEffect(() => {
    document.title = 'AKAR TANI · Data Bahan Organik'
  }, [])

  const rows = useMemo(() => {
    if (!data) return []
    const q = query.trim().toLowerCase()
    if (!q) return data
    return data.filter(
      (d) =>
        d.jenis_bahan_organik.toLowerCase().includes(q) ||
        (d.kategori_bahan ?? '').toLowerCase().includes(q) ||
        (d.bahan_id ?? '').toLowerCase().includes(q),
    )
  }, [data, query])

  return (
    <div className="page">
      <Card>
        <CardHeader
          title="Data Bahan Organik"
          subtitle="Ketersediaan bahan organik hasil analisis"
        />
        <div className="toolbar">
          <input
            type="search"
            className="input"
            placeholder="Cari bahan atau kategori…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Cari bahan organik"
          />
          <span className="toolbar__count tnum">{rows.length} baris</span>
        </div>

        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState detail={error} onRetry={refetch} />
        ) : rows.length === 0 ? (
          <EmptyState
            title="Tidak ada hasil"
            detail={
              query
                ? 'Coba kata kunci lain.'
                : 'Belum ada data bahan organik.'
            }
          />
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Jenis Bahan Organik</th>
                  <th>Kategori</th>
                  <th className="tnum">Ketersediaan</th>
                  <th>Satuan</th>
                  <th>Kontinuitas</th>
                  <th className="tnum">Jarak (km)</th>
                  <th>Pengumpulan</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => (
                  <tr key={`${r.bahan_id}-${i}`}>
                    <td className="tnum muted">{r.bahan_id}</td>
                    <td className="strong">{r.jenis_bahan_organik}</td>
                    <td>{r.kategori_bahan ?? '—'}</td>
                    <td className="tnum">
                      {r.jumlah_ketersediaan != null
                        ? formatNumber(r.jumlah_ketersediaan)
                        : '—'}
                    </td>
                    <td>{r.satuan ?? '—'}</td>
                    <td>{r.kontinuitas ?? '—'}</td>
                    <td className="tnum">
                      {r.jarak_ke_produksi_km != null
                        ? r.jarak_ke_produksi_km.toFixed(1)
                        : '—'}
                    </td>
                    <td>{r.kemudahan_pengumpulan ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}