import { useEffect, useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { LoadingState, ErrorState, EmptyState } from '../components/States'
import {
  PredictionMonthlyChart,
  PredictionSummaryChart,
} from '../features/prediction'
import { formatNumber } from '../utils/format'

export function PrediksiPage() {
  const prediction = useFetch(() => api.getPrediction2026())
  const summary = useFetch(() => api.getPredictionSummary())
  const [selected, setSelected] = useState('semua')

  useEffect(() => {
    document.title = 'AKAR TANI · Prediksi Kebutuhan Pupuk'
  }, [])

  const products = summary.data ?? []
  const filtered =
    selected === 'semua'
      ? prediction.data ?? []
      : (prediction.data ?? []).filter((e) => e.produk === selected)

  const totalPrediction = summary.data?.reduce((s, p) => s + p.total_prediksi, 0) ?? 0
  const model = prediction.data?.[0]?.model

  return (
    <div className="page">
      <div className="stack">
        <Card>
          <CardHeader
            title="Prediksi Penjualan Bulanan 2026"
            subtitle={
              `Total ${formatNumber(Math.round(totalPrediction))} unit · 11 produk` +
              (selected !== 'semua' ? ` · filter: ${selected}` : '')
            }
          />
          <div className="toolbar">
            <label className="toolbar__label" htmlFor="produk-filter">
              Produk
            </label>
            <select
              id="produk-filter"
              className="input"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              <option value="semua">Semua produk</option>
              {products.map((p) => (
                <option key={p.produk} value={p.produk}>
                  {p.produk}
                </option>
              ))}
            </select>
          </div>

          {prediction.loading ? (
            <LoadingState />
          ) : prediction.error ? (
            <ErrorState detail={prediction.error} onRetry={prediction.refetch} />
          ) : filtered.length > 0 ? (
            <>
              <PredictionMonthlyChart data={filtered} />
              {model && (
                <p className="viz-note">
                  Model: {model} · nilai prediksi diperbarui dari pipeline
                  machine learning.
                </p>
              )}
            </>
          ) : (
            <EmptyState />
          )}
        </Card>

        <Card>
          <CardHeader
            title="Perkiraan per Produk"
            subtitle="Perbandingan total prediksi tiap produk, diurutkan"
          />
          {summary.loading ? (
            <LoadingState />
          ) : summary.error ? (
            <ErrorState detail={summary.error} onRetry={summary.refetch} />
          ) : summary.data && summary.data.length > 0 ? (
            <PredictionSummaryChart data={summary.data} />
          ) : (
            <EmptyState />
          )}
        </Card>
      </div>
    </div>
  )
}