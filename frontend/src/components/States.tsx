import { AlertTriangle, Inbox, RefreshCw } from 'lucide-react'

/**
 * Normalized loading / empty / error states used across the app.
 */

export function LoadingState({
  label = 'Memuat data…',
}: {
  label?: string
}) {
  return (
    <div className="state" role="status" aria-live="polite">
      <span className="state__spinner" aria-hidden="true" />
      <span className="state__label">{label}</span>
    </div>
  )
}

export function EmptyState({
  title = 'Belum ada data',
  detail,
}: {
  title?: string
  detail?: string
}) {
  return (
    <div className="state">
      <span className="state__icon" aria-hidden="true">
        <Inbox size={22} />
      </span>
      <span className="state__title">{title}</span>
      {detail && <span className="state__detail">{detail}</span>}
    </div>
  )
}

export function ErrorState({
  title = 'Data tidak dapat dimuat',
  detail,
  onRetry,
}: {
  title?: string
  detail?: string
  onRetry?: () => void
}) {
  return (
    <div className="state" role="alert">
      <span className="state__icon state__icon--danger" aria-hidden="true">
        <AlertTriangle size={22} />
      </span>
      <span className="state__title">{title}</span>
      {detail && <span className="state__detail">{detail}</span>}
      {onRetry && (
        <button type="button" className="btn btn--ghost" onClick={onRetry}>
          <RefreshCw size={15} aria-hidden="true" />
          Coba lagi
        </button>
      )}
    </div>
  )
}