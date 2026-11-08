import { Outlet, useLocation } from 'react-router-dom'
import { Sidebar, MobileHeader } from './Sidebar'
import { Header, headerFor } from './Header'
import { ErrorBoundary } from './ErrorBoundary'

export function AppLayout() {
  const { pathname } = useLocation()
  const { title, subtitle } = headerFor(pathname)
  return (
    <div className="app">
      <Sidebar />
      <MobileHeader />
      <div className="app__main">
        <Header title={title} subtitle={subtitle} />
        <main className="app__content">
          <ErrorBoundary key={pathname}>
            <Outlet />
          </ErrorBoundary>
        </main>
      </div>
    </div>
  )
}