import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Boxes, Leaf, Package, Sprout, TrendingUp } from 'lucide-react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { LoadingState, ErrorState, EmptyState } from '../components/States'
import { LandscapePanel } from '../components/LandscapePanel'
import { RankingList } from '../features/ranking/RankingList'
import {
  PredictionMonthlyChart,
  PredictionSummaryChart,
} from '../features/prediction'
import { ProductCard } from '../features/catalog/ProductCard'
import { formatNumber } from '../utils/format'
import type { DashboardSummary } from '../api/types'

interface Kpi {
  key: keyof DashboardSummary
  label: string
  icon: typeof Boxes
  tone: 'green' | 'blue' | 'sun'
}

const KPIS: Kpi[] = [
  { key: 'total_bahan_organik', label: 'Bahan Organik', icon: Sprout, tone: 'green' },
  { key: 'total_produk', label: 'Produk Katalog', icon: Package, tone: 'sun' },
  { key: 'total_data_produksi', label: 'Data Produksi', icon: Boxes, tone: 'green' },
  { key: 'total_data_penjualan', label: 'Data Penjualan', icon: TrendingUp, tone: 'blue' },
]

export function DashboardPage() {
  const summary = useFetch(() => api.getDashboardSummary())
  const ranking = useFetch(() => api.getOrganicRanking())
  const prediction = useFetch(() => api.getPrediction2026())
  const predSummary = useFetch(() => api.getPredictionSummary())
  const products = useFetch(() => api.getProducts())

  useEffect(() => {
    document.title = 'AKAR TANI · Dashboard'
  }, [])

  const totalPrediction =
    predSummary.data?.reduce((s, p) => s + p.total_prediksi, 0) ?? 0

  return (
    <div className="dash">
      {/* Welcome banner — hero-akar-tani.png as background */}
      <section className="welcome">
        <div className="welcome__inner">
          <span className="welcome__eyebrow">
            <Leaf size={13} aria-hidden="true" />
            Pertanian Terpadu
          </span>
          <h1 className="welcome__title">Selamat Datang di AKAR TANI</h1>
          <p className="welcome__lead">
            Sistem Informasi dan Pengembangan Usaha Pertanian
          </p>
          <p className="welcome__support">
            Platform terintegrasi Desa Cangkringan untuk memantau bahan organik,
            produksi, penjualan, dan prediksi kebutuhan pupuk dalam satu
            dasbor.
          </p>
          <div className="welcome__stats">
            {summary.data && (
              <span className="welcome__stat">
                <strong className="tnum">
                  {formatNumber(summary.data.total_bahan_organik)}
                </strong>{' '}
                bahan organik
              </span>
            )}
            {summary.data && (
              <span className="welcome__stat">
                <strong className="tnum">
                  {formatNumber(summary.data.total_produk)}
                </strong>{' '}
                produk katalog
              </span>
            )}
            {totalPrediction > 0 && (
              <span className="welcome__stat">
                <strong className="tnum">
                  {formatNumber(Math.round(totalPrediction))}
                </strong>{' '}
                unit perkiraan 2026
              </span>
            )}
          </div>
        </div>
      </section>

      {/* KPI cards */}
      <section className="kpi-grid" aria-label="Ringkasan data">
        {summary.loading ? (
          <LoadingState label="Memuat ringkasan…" />
        ) : summary.error ? (
          <ErrorState detail={summary.error} onRetry={summary.refetch} />
        ) : summary.data ? (
          KPIS.map((k) => {
            const Icon = k.icon
            const value = summary.data![k.key]
            return (
              <Card key={k.key} className="kpi">
                <span className={`kpi__icon kpi__icon--${k.tone}`} aria-hidden="true">
                  <Icon size={20} strokeWidth={2} />
                </span>
                <span className="kpi__value tnum">{formatNumber(value)}</span>
                <span className="kpi__label">{k.label}</span>
              </Card>
            )
          })
        ) : (
          <EmptyState />
        )}
      </section>

      {/* Workspace + landscape panel */}
      <div className="dash__grid">
        <div className="dash__col">
          <Card>
            <CardHeader
              title="Analisis Potensi Bahan Organik"
              subtitle="Peringkat lima teratas berdasarkan skor SAW"
              action={
                <Link to="/analisis" className="textlink">
                  Selengkapnya <ArrowRight size={14} aria-hidden="true" />
                </Link>
              }
            />
            {ranking.loading ? (
              <LoadingState />
            ) : ranking.error ? (
              <ErrorState detail={ranking.error} onRetry={ranking.refetch} />
            ) : ranking.data && ranking.data.length > 0 ? (
              <RankingList data={ranking.data} limit={5} />
            ) : (
              <EmptyState />
            )}
          </Card>

          <Card>
            <CardHeader
              title="Prediksi Penjualan 2026"
              subtitle="Total perkiraan penjualan bulanan"
              action={
                <Link to="/prediksi" className="textlink">
                  Detail <ArrowRight size={14} aria-hidden="true" />
                </Link>
              }
            />
            {prediction.loading ? (
              <LoadingState />
            ) : prediction.error ? (
              <ErrorState detail={prediction.error} onRetry={prediction.refetch} />
            ) : prediction.data && prediction.data.length > 0 ? (
              <PredictionMonthlyChart data={prediction.data} />
            ) : (
              <EmptyState />
            )}
          </Card>

          <Card>
            <CardHeader
              title="Perkiraan per Produk"
              subtitle="Total prediksi tiap produk, diurutkan"
              action={
                <Link to="/produksi-penjualan" className="textlink">
                  Ringkasan <ArrowRight size={14} aria-hidden="true" />
                </Link>
              }
            />
            {predSummary.loading ? (
              <LoadingState />
            ) : predSummary.error ? (
              <ErrorState detail={predSummary.error} onRetry={predSummary.refetch} />
            ) : predSummary.data && predSummary.data.length > 0 ? (
              <PredictionSummaryChart data={predSummary.data} />
            ) : (
              <EmptyState />
            )}
          </Card>

          <Card>
            <CardHeader
              title="Katalog Produk"
              subtitle="Pratinjau produk pupuk dan probiotik dari desa"
              action={
                <Link to="/katalog" className="textlink">
                  Lihat semua <ArrowRight size={14} aria-hidden="true" />
                </Link>
              }
            />
            {products.loading ? (
              <LoadingState />
            ) : products.error ? (
              <ErrorState detail={products.error} onRetry={products.refetch} />
            ) : products.data && products.data.length > 0 ? (
              <div className="pcards">
                {products.data.slice(0, 3).map((p) => (
                  <ProductCard key={p.produk_id} product={p} />
                ))}
              </div>
            ) : (
              <EmptyState />
            )}
          </Card>
        </div>

        <aside className="dash__side">
          <LandscapePanel
            ranking={ranking.data}
            predSummary={predSummary.data}
            loading={ranking.loading || predSummary.loading}
          />
        </aside>
      </div>
    </div>
  )
}
