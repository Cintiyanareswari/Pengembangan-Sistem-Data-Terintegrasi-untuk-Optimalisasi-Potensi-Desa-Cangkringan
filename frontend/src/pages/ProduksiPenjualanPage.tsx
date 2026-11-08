import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Card, CardHeader } from '../components/Card'
import { ErrorState } from '../components/States'
import { ArrowRight, Factory, ReceiptText } from 'lucide-react'
import { formatNumber } from '../utils/format'

/**
 * Produksi & Penjualan overview. Counts come from the dashboard summary;
 * the dedicated prediction figures come from /prediction/summary.
 * There is no /produksi or /penjualan list endpoint, so we present the
 * verified aggregate counts without inventing non-existent detail rows.
 */
export function ProduksiPenjualanPage() {
  const summary = useFetch(() => api.getDashboardSummary())
  const predSummary = useFetch(() => api.getPredictionSummary())

  useEffect(() => {
    document.title = 'AKAR TANI · Produksi & Penjualan'
  }, [])

  const totalPrediction =
    predSummary.data?.reduce((s, p) => s + p.total_prediksi, 0) ?? 0

  return (
    <div className="page">
      <div className="stack">
        <div className="two-cols">
          <Card className="metric-card">
            <span className="metric-card__icon metric-card__icon--green" aria-hidden="true">
              <Factory size={22} />
            </span>
            <div>
              <span className="metric-card__value tnum">
                {summary.loading
                  ? '—'
                  : formatNumber(summary.data?.total_data_produksi ?? 0)}
              </span>
              <span className="metric-card__label">catatan produksi pupuk</span>
            </div>
          </Card>

          <Card className="metric-card">
            <span className="metric-card__icon metric-card__icon--blue" aria-hidden="true">
              <ReceiptText size={22} />
            </span>
            <div>
              <span className="metric-card__value tnum">
                {summary.loading
                  ? '—'
                  : formatNumber(summary.data?.total_data_penjualan ?? 0)}
              </span>
              <span className="metric-card__label">catatan penjualan</span>
            </div>
          </Card>
        </div>

        {summary.error && (
          <Card>
            <ErrorState detail={summary.error} onRetry={summary.refetch} />
          </Card>
        )}

        <Card>
          <CardHeader
            title="Ringkasan Produksi & Penjualan"
            subtitle="Indikator utama tersedia dari data terpadu desa"
          />
          <div className="notice">
            <p>
              Perkiraan total produksi pupuk untuk tahun 2026 adalah{' '}
              <strong className="tnum">{formatNumber(Math.round(totalPrediction))}</strong>{' '}
              unit, dihitung dari model prediksi penjualan yang telah dilatih.
            </p>
            <p className="notice__muted">
              Data produksi dan penjualan historis tersimpan di database; detail
              per-bulan dan per-produk dapat dilihat pada halaman{' '}
              <Link to="/prediksi" className="textlink">
                Prediksi Kebutuhan Pupuk <ArrowRight size={13} aria-hidden="true" />
              </Link>
              .
            </p>
          </div>
        </Card>

        {predSummary.data && predSummary.data.length > 0 && (
          <Card>
            <CardHeader
              title="Perkiraan produksi per produk (2026)"
              subtitle="Total prediksi penjualan per produk, tertinggi ke terendah"
            />
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>Produk</th>
                    <th className="tnum">Total perkiraan (unit)</th>
                  </tr>
                </thead>
                <tbody>
                  {[...predSummary.data]
                    .sort((a, b) => b.total_prediksi - a.total_prediksi)
                    .map((p) => (
                      <tr key={p.produk}>
                        <td className="strong">{p.produk}</td>
                        <td className="tnum">
                          {formatNumber(Math.round(p.total_prediksi))}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}