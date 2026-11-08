import type { LucideIcon } from 'lucide-react'
import {
  Boxes,
  FlaskConical,
  LayoutDashboard,
  LineChart,
  ShoppingBag,
  TrendingUp,
} from 'lucide-react'

export interface NavItem {
  to: string
  label: string
  icon: LucideIcon
  end?: boolean
}

/**
 * Navigation model — drives both the sidebar and page titles.
 * Routes use English slugs (URL-stable) with Indonesian labels.
 */
export const NAV_ITEMS: NavItem[] = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/bahan-organik', label: 'Data Bahan Organik', icon: Boxes },
  {
    to: '/analisis',
    label: 'Analisis Potensi Bahan Organik',
    icon: FlaskConical,
  },
  { to: '/produksi-penjualan', label: 'Produksi & Penjualan', icon: TrendingUp },
  { to: '/prediksi', label: 'Prediksi Kebutuhan Pupuk', icon: LineChart },
  { to: '/katalog', label: 'Katalog Produk', icon: ShoppingBag },
]