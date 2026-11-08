import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import {
  BadgeCheck,
  Boxes,
  Factory,
  MapPin,
  Package,
  Phone,
  Tag,
  X,
} from 'lucide-react'
import { useFetch } from '../../hooks/useFetch'
import { api } from '../../api/client'
import { LoadingState, ErrorState } from '../../components/States'
import { formatRupiah, titleCase } from '../../utils/format'
import { productPhotoUrl } from './productPhotos'

/**
 * Product detail as a modal dialog.
 *
 * The app's router has no product-detail route (six fixed pages + 404),
 * so a dialog is the shape that fits: it adds no route, keeps the catalog
 * mounted behind it, and works the same for mouse and touch.
 *
 * All values come from GET /catalog/products/{produk_id}. Fields the API
 * leaves null are simply not rendered — never filled with a placeholder.
 */
export function ProductDetailDialog({
  produkId,
  onClose,
}: {
  produkId: string
  onClose: () => void
}) {
  const detail = useFetch(() => api.getProductById(produkId))
  const [broken, setBroken] = useState(false)
  const closeRef = useRef<HTMLButtonElement>(null)
  const restoreRef = useRef<HTMLElement | null>(null)

  const product = detail.data
  const photo = product
    ? productPhotoUrl(product.produk_id, product.nama_produk)
    : null

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

  // Lock background scroll, move focus into the dialog, and hand focus
  // back to whatever opened it on unmount.
  useEffect(() => {
    restoreRef.current = document.activeElement as HTMLElement | null
    const prevOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeRef.current?.focus()
    return () => {
      document.body.style.overflow = prevOverflow
      restoreRef.current?.focus?.()
    }
  }, [])

  const titleId = `pdetail-title-${produkId}`

  return createPortal(
    <div className="modal">
      <button
        type="button"
        className="modal__scrim"
        aria-label="Tutup detail produk"
        onClick={onClose}
      />
      <div
        className="modal__dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
      >
        <button
          type="button"
          ref={closeRef}
          className="modal__close"
          aria-label="Tutup detail produk"
          onClick={onClose}
        >
          <X size={18} aria-hidden="true" />
        </button>

        {detail.loading ? (
          <LoadingState label="Memuat detail produk…" />
        ) : detail.error ? (
          <div className="modal__state">
            <ErrorState detail={detail.error} onRetry={detail.refetch} />
          </div>
        ) : product ? (
          <div className="modal__grid">
            <div className="modal__media">
              {photo && !broken ? (
                <img
                  className="modal__photo"
                  src={photo}
                  alt={`Foto ${product.nama_produk}`}
                  onError={() => setBroken(true)}
                />
              ) : (
                <span className="modal__fallback" aria-hidden="true">
                  <Package size={40} strokeWidth={1.4} />
                </span>
              )}
            </div>

            <div className="modal__body">
              <div className="modal__head">
                {product.jenis_produk && (
                  <span className="modal__tag">
                    {titleCase(product.jenis_produk)}
                  </span>
                )}
                <h2 className="modal__title" id={titleId}>
                  {product.nama_produk}
                </h2>
                <span className="modal__id tnum">#{product.produk_id}</span>
              </div>

              <div className="modal__facts">
                {product.harga != null && (
                  <span className="modal__fact modal__fact--price">
                    <Tag size={14} aria-hidden="true" />
                    <span className="tnum">{formatRupiah(product.harga)}</span>
                  </span>
                )}
                {product.stok_ketersediaan && (
                  <span className="modal__fact modal__fact--ok">
                    <BadgeCheck size={14} aria-hidden="true" />
                    {product.stok_ketersediaan}
                  </span>
                )}
                {product.ukuran_kemasan && (
                  <span className="modal__fact">
                    <Boxes size={14} aria-hidden="true" />
                    {product.ukuran_kemasan}
                  </span>
                )}
              </div>

              {product.deskripsi && (
                <section className="modal__section">
                  <h3 className="modal__label">Deskripsi</h3>
                  <p className="modal__text">{product.deskripsi}</p>
                </section>
              )}

              {product.manfaat && (
                <section className="modal__section">
                  <h3 className="modal__label">Manfaat</h3>
                  <p className="modal__text">{product.manfaat}</p>
                </section>
              )}

              {(product.produsen ||
                product.lokasi_produsen ||
                product.kontak) && (
                <section className="modal__section">
                  <h3 className="modal__label">Produsen</h3>
                  <ul className="modal__meta">
                    {product.produsen && (
                      <li>
                        <Factory size={14} aria-hidden="true" />
                        {product.produsen}
                      </li>
                    )}
                    {product.lokasi_produsen && (
                      <li>
                        <MapPin size={14} aria-hidden="true" />
                        {product.lokasi_produsen}
                      </li>
                    )}
                    {product.kontak && (
                      <li>
                        <Phone size={14} aria-hidden="true" />
                        {product.kontak}
                      </li>
                    )}
                  </ul>
                </section>
              )}

              <div className="modal__actions">
                <button type="button" className="btn btn--ghost" onClick={onClose}>
                  Tutup
                </button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>,
    document.body,
  )
}
