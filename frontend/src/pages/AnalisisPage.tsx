import { useEffect, useMemo } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { LoadingState, ErrorState, EmptyState } from '../components/States'
import { RankingList } from '../features/ranking/RankingList'
import { formatScore, formatNumber } from '../utils/format'

export function AnalisisPage() {
  const ranking = useFetch(() => api.getOrganicRanking())
  const analysis = useFetch(() => api.getOrganicAnalysis())

  useEffect(() => {
    document.title = 'AKAR TANI · Analisis Potensi Bahan Organik'
  }, [])

  const summary = useMemo(() => {
    if (!ranking.data) return null
    const top = ranking.data[0]
    const avg =
      ranking.data.reduce((s, r) => s + r.skor_akhir, 0) / ranking.data.length
    return { top, count: ranking.data.length, avg }
  }, [ranking.data])

  return (
    <div className="page page--split">
      <div className="page__col">
        <Card>
          <CardHeader
            title="Peringkat Bahan Organik"
            subtitle="Hasil pembobotan AHP dan skoring SAW"
          />
          {ranking.loading ? (
            <LoadingState />
          ) : ranking.error ? (
            <ErrorState detail={ranking.error} onRetry={ranking.refetch} />
          ) : ranking.data && ranking.data.length > 0 ? (
            <RankingList data={ranking.data} />
          ) : (
            <EmptyState />
          )}
        </Card>
      </div>

      <div className="page__col">
        {summary && (
          <Card className="stat-cards">
            <div className="stat-mini">
              <span className="stat-mini__label">Peringkat pertama</span>
              <span className="stat-mini__value">{summary.top.jenis_bahan_organik}</span>
              <span className="stat-mini__meta tnum">
                Skor {formatScore(summary.top.skor_akhir)}
              </span>
            </div>
            <div className="stat-mini">
              <span className="stat-mini__label">Jumlah bahan</span>
              <span className="stat-mini__value tnum">{summary.count}</span>
              <span className="stat-mini__meta">jenis bahan organik</span>
            </div>
            <div className="stat-mini">
              <span className="stat-mini__label">Rata-rata skor</span>
              <span className="stat-mini__value tnum">
                {formatScore(summary.avg)}
              </span>
              <span className="stat-mini__meta">skor SAW</span>
            </div>
          </Card>
        )}

        <Card>
          <CardHeader
            title="Ketersediaan Bahan"
            subtitle={`${analysis.data?.length ?? 0} catatan ketersediaan`}
          />
          {analysis.loading ? (
            <LoadingState />
          ) : analysis.error ? (
            <ErrorState detail={analysis.error} onRetry={analysis.refetch} />
          ) : analysis.data && analysis.data.length > 0 ? (
            <div className="table-wrap table-wrap--compact">
              <table className="table table--tight">
                <thead>
                  <tr>
                    <th>Bahan</th>
                    <th className="tnum">Jumlah</th>
                    <th>Kontinuitas</th>
                  </tr>
                </thead>
                <tbody>
                  {analysis.data.slice(0, 12).map((r, i) => (
                    <tr key={`${r.bahan_id}-${i}`}>
                      <td className="strong">{r.jenis_bahan_organik}</td>
                      <td className="tnum nowrap">
                        {r.jumlah_ketersediaan != null
                          ? `${formatNumber(r.jumlah_ketersediaan)} ${r.satuan ?? ''}`.trim()
                          : '—'}
                      </td>
                      <td>{r.kontinuitas ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState />
          )}
        </Card>
      </div>
    </div>
  )
}