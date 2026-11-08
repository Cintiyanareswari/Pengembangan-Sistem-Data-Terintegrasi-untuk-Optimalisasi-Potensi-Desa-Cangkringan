import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Card } from '../components/Card'

export function NotFoundPage() {
  useEffect(() => {
    document.title = 'AKAR TANI · Halaman tidak ditemukan'
  }, [])

  return (
    <div className="page">
      <Card className="notfound">
        <h2 className="notfound__code">404</h2>
        <p className="notfound__title">Halaman tidak ditemukan</p>
        <p className="notfound__text">
          Halaman yang Anda tuju tidak ada. Periksa kembali alamatnya.
        </p>
        <Link to="/" className="btn btn--primary">
          Kembali ke Dashboard
        </Link>
      </Card>
    </div>
  )
}