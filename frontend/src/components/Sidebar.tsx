import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import { BrandLogo } from './BrandLogo'
import { NAV_ITEMS } from './nav'

function SidebarBody({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <>
      <BrandLogo />
      <nav className="sidebar__nav" aria-label="Navigasi utama">
        <ul className="sidebar__list">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            return (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  onClick={onNavigate}
                  className={({ isActive }) =>
                    `sidebar__link${isActive ? ' is-active' : ''}`
                  }
                >
                  <Icon size={19} strokeWidth={2} className="sidebar__link-icon" />
                  <span>{item.label}</span>
                </NavLink>
              </li>
            )
          })}
        </ul>
      </nav>
      <div className="sidebar__foot">
        <p className="sidebar__foot-label">Sistem informasi</p>
        <p className="sidebar__foot-text">
          Terintegrasi untuk desa — bahan organik, produksi, dan prediksi pupuk.
        </p>
      </div>
    </>
  )
}

export function Sidebar() {
  return (
    <aside className="sidebar">
      <SidebarBody />
    </aside>
  )
}

export function MobileHeader() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <header className="mobile-top">
        <BrandLogo />
        <button
          type="button"
          className="mobile-top__toggle"
          aria-label="Buka menu navigasi"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </header>

      {open && (
        <div className="mobile-drawer">
          <button
            type="button"
            className="mobile-drawer__scrim"
            aria-label="Tutup menu"
            onClick={() => setOpen(false)}
          />
          <div className="mobile-drawer__panel sidebar">
            <SidebarBody onNavigate={() => setOpen(false)} />
          </div>
        </div>
      )}
    </>
  )
}