import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Card } from './Card'
import { ErrorState } from './States'

interface Props {
  children: ReactNode
}

interface State {
  error: Error | null
}

/**
 * Catches render-time errors so a single broken view shows a
 * recoverable message instead of a blank screen or raw stack trace.
 */
export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null }

  static getDerivedStateFromError(error: Error): State {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('AKAR TANI render error:', error, info.componentStack)
  }

  render() {
    if (this.state.error) {
      return (
        <div className="page">
          <Card>
            <ErrorState
              title="Terjadi kesalahan pada halaman ini"
              detail="Muat ulang halaman untuk mencoba lagi."
              onRetry={() => this.setState({ error: null })}
            />
          </Card>
        </div>
      )
    }
    return this.props.children
  }
}