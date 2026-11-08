// Formatting helpers for Indonesian locale.

const MONTHS_ID = [
  'Januari',
  'Februari',
  'Maret',
  'April',
  'Mei',
  'Juni',
  'Juli',
  'Agustus',
  'September',
  'Oktober',
  'November',
  'Desember',
]

export function formatNumber(n: number): string {
  return new Intl.NumberFormat('id-ID').format(n)
}

export function formatRupiah(value: number | string | null | undefined): string {
  if (value === null || value === undefined) return '—'
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (Number.isNaN(num)) return '—'
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(num)
}

export function formatDateLong(date: Date = new Date()): string {
  const day = date.getDate()
  const month = MONTHS_ID[date.getMonth()]
  const year = date.getFullYear()
  return `${day} ${month} ${year}`
}

export function formatMonthLabel(isoMonth: string): string {
  // input like "2026-01-01" — only the year+month matter for a monthly axis
  const [year, month] = isoMonth.split('-')
  const m = parseInt(month, 10) - 1
  if (Number.isNaN(m) || m < 0 || m > 11) return isoMonth.slice(0, 7)
  return `${MONTHS_ID[m].slice(0, 3)} ${year}`
}

export function formatScore(score: number): string {
  return score.toLocaleString('id-ID', {
    minimumFractionDigits: 3,
    maximumFractionDigits: 3,
  })
}

export function titleCase(value: string): string {
  return value.replace(/\w\S*/g, (t) => t.charAt(0).toUpperCase() + t.slice(1))
}