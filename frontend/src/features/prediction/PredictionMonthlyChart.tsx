import { useMemo } from 'react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts'
import type { PredictionEntry } from '../../api/types'
import { formatMonthLabel, formatNumber } from '../../utils/format'

type Row = { bulan: string; label: string; total: number }

/**
 * Monthly aggregate of predicted 2026 sales. Sums the 11 products
 * for each of the 12 months. Values are model predictions, not guarantees.
 */
export function PredictionMonthlyChart({ data }: { data: PredictionEntry[] }) {
  const rows: Row[] = useMemo(() => {
    const byMonth = new Map<string, number>()
    for (const e of data) {
      const key = e.bulan.slice(0, 7) // YYYY-MM
      byMonth.set(key, (byMonth.get(key) ?? 0) + e.prediksi_penjualan)
    }
    return Array.from(byMonth.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([k, v]) => ({
        bulan: k,
        label: formatMonthLabel(`${k}-01`),
        total: Math.round(v * 100) / 100,
      }))
  }, [data])

  return (
    <div className="viz" role="img" aria-label="Grafik prediksi penjualan bulanan tahun 2026">
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={rows} margin={{ top: 8, right: 8, left: -14, bottom: 0 }}>
          <defs>
            <linearGradient id="predFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--chart-fill)" stopOpacity={0.24} />
              <stop offset="100%" stopColor="var(--chart-fill)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid
            vertical={false}
            stroke="var(--border)"
            strokeDasharray="3 3"
          />
          <XAxis
            dataKey="label"
            tickLine={false}
            axisLine={false}
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            interval="preserveStartEnd"
          />
          <YAxis
            tickLine={false}
            axisLine={false}
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            tickFormatter={(v: number) => formatNumber(v)}
          />
          <Tooltip
            cursor={{ stroke: 'var(--green-300)', strokeWidth: 1 }}
            formatter={(value: number) => [formatNumber(value), 'Prediksi']}
            labelFormatter={(_, payload) =>
              payload?.[0]?.payload?.bulan ?? ''
            }
            contentStyle={{
              borderRadius: 10,
              border: '1px solid var(--border)',
              boxShadow: 'var(--shadow-md)',
              fontSize: 12,
            }}
          />
          <Area
            type="monotone"
            dataKey="total"
            stroke="var(--green-500)"
            strokeWidth={2.4}
            fill="url(#predFill)"
            dot={false}
            activeDot={{ r: 4, strokeWidth: 0 }}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}