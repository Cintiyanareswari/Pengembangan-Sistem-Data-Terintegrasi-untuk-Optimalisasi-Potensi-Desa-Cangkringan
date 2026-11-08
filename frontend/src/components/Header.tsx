import { NAV_ITEMS } from './nav'
import { formatDateLong } from '../utils/format'
import { CalendarDays } from 'lucide-react'

export function Header({
  title,
  subtitle,
}: {
  title?: string
  subtitle?: string
}) {
  return (
    <header className="pagehead">
      <div className="pagehead__title">
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      <div className="pagehead__date" title="Tanggal hari ini">
        <CalendarDays size={16} aria-hidden="true" />
        <span>{formatDateLong()}</span>
      </div>
    </header>
  )
}

export function headerFor(path: string): { title: string; subtitle: string } {
  const item = NAV_ITEMS.find((n) =>
    n.end ? path === n.to : path.startsWith(n.to),
  )
  const fallback = 'AKAR TANI'
  if (!item) return { title: fallback, subtitle: '' }
  if (item.to === '/') {
    return { title: fallback, subtitle: '' }
  }
  return { title: item.label, subtitle: 'Desa Cangkringan' }
}
