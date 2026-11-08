import { useMemo } from 'react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from 'recharts'
import type { PredictionSummary } from '../../api/types'
import { formatNumber } from '../../utils/format'

type Row = { produk: string; total: number; short: string }

function shorten(name: string): string {
  const cut = 22
  return name.length > cut ? `${name.slice(0, cut)}…` : name
}

/**
 * Product-level predicted demand for 2026 (from /prediction/summary).
 * Ordered highest first; top bar emphasized, rest on a green fill.
 *
 * Needs a full-width column: label truncation is what distinguishes the
 * eleven products, so a narrower host makes them indistinguishable.
 */
export function PredictionSummaryChart({ data }: { data: PredictionSummary[] }) {
  const rows: Row[] = useMemo(
    () =>
      data
        .map((d) => ({
          produk: d.produk,
          total: Math.round(d.total_prediksi * 100) / 100,
          short: shorten(d.produk),
        }))
        .sort((a, b) => b.total - a.total),
    [data],
  )

  return (
    <div className="viz" role="img" aria-label="Grafik total prediksi penjualan per produk tahun 2026">
      <ResponsiveContainer width="100%" height={Math.max(rows.length * 34, 180)}>
        <BarChart
          data={rows}
          layout="vertical"
          margin={{ top: 4, right: 20, left: 8, bottom: 0 }}
        >
          <CartesianGrid horizontal={false} stroke="var(--border)" strokeDasharray="3 3" />
          <XAxis
            type="number"
            tickLine={false}
            axisLine={false}
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            tickFormatter={(v: number) => formatNumber(v)}
          />
          <YAxis
            type="category"
            dataKey="short"
            width={200}
            tickLine={false}
            axisLine={false}
            tick={{ fill: 'var(--text-primary)', fontSize: 12 }}
          />
          <Tooltip
            cursor={{ fill: 'var(--sky)' }}
            formatter={(value: number) => [formatNumber(value), 'Prediksi']}
            labelFormatter={(_, payload) =>
              payload?.[0]?.payload?.produk ?? ''
            }
            contentStyle={{
              borderRadius: 10,
              border: '1px solid var(--border)',
              boxShadow: 'var(--shadow-md)',
              fontSize: 12,
            }}
          />
          <Bar
            dataKey="total"
            radius={[0, 4, 4, 0]}
            barSize={18}
            isAnimationActive={false}
          >
            {rows.map((r, i) => (
              /* Top product takes the validated blue accent; the rest read
                 as one green ramp so the series stays single-hue. */
              <Cell
                key={r.produk}
                fill={i === 0 ? 'var(--chart-alt)' : 'var(--green-300)'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}