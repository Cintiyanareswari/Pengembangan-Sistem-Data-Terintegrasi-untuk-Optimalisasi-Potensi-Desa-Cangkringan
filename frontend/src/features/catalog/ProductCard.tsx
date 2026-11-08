import { useState } from 'react'
import type { Product } from '../../api/types'
import { formatRupiah, titleCase } from '../../utils/format'
import { Package, MapPin } from 'lucide-react'
import { productPhotoUrl } from './productPhotos'

/**
 * Product card. Renders the real product photograph when one is mapped
 * (see productPhotos.ts); otherwise falls back to a designed identity
 * tile so a missing asset never shows a broken image.
 *
 * The whole card opens the detail dialog via a transparent "stretched"
 * button rather than by making the card itself interactive: the visible
 * copy stays in the accessibility tree, there are no nested controls,
 * and the target is the full card on touch screens.
 */
export function ProductCard({
  product,
  onOpen,
}: {
  product: Product
  onOpen?: (produkId: string) => void
}) {
  const jenis = product.jenis_produk ? titleCase(product.jenis_produk) : 'Produk'
  const isAvailable =
    product.stok_ketersediaan?.toLowerCase().trim() === 'tersedia'
  const photo = productPhotoUrl(product.produk_id, product.nama_produk)
  const [broken, setBroken] = useState(false)

  return (
    <article className="pcard">
      <div className="pcard__visual">
        {photo && !broken ? (
          <img
            className="pcard__photo"
            src={photo}
            alt={`Foto ${product.nama_produk}`}
            loading="lazy"
            onError={() => setBroken(true)}
          />
        ) : (
          <span className="pcard__fallback" aria-hidden="true">
            <Package size={28} strokeWidth={1.6} />
          </span>
        )}
        <span className="pcard__tag">{jenis}</span>
      </div>
      <div className="pcard__body">
        <div className="pcard__top">
          <span className="pcard__id tnum">#{product.produk_id}</span>
          <span
            className={`pcard__stock ${isAvailable ? 'is-ok' : ''}`}
            title={product.stok_ketersediaan ?? '—'}
          >
            {product.stok_ketersediaan ?? 'Ketersediaan —'}
          </span>
        </div>
        <h3 className="pcard__name">{product.nama_produk}</h3>
        {product.deskripsi && <p className="pcard__desc">{product.deskripsi}</p>}
        <div className="pcard__foot">
          <span className="pcard__price tnum">{formatRupiah(product.harga)}</span>
          {product.lokasi_produsen && (
            <span className="pcard__loc">
              <MapPin size={12} aria-hidden="true" />
              {product.lokasi_produsen}
            </span>
          )}
        </div>
      </div>

      {onOpen && (
        <button
          type="button"
          className="pcard__open"
          onClick={() => onOpen(product.produk_id)}
        >
          <span className="sr-only">Lihat detail {product.nama_produk}</span>
        </button>
      )}
    </article>
  )
}
