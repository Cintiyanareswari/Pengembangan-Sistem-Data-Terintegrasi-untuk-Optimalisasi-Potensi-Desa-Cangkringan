import { MapPin, BadgeCheck, Layers } from 'lucide-react'
import type { OrganicRanking, PredictionSummary } from '../api/types'
import { LOGO_SRC } from './BrandLogo'
import { formatNumber } from '../utils/format'

/**
 * Right-hand contextual panel: a dark agricultural landscape with real
 * data on top of it. Purely presentational — every number comes from
 * props already fetched by the dashboard.
 *
 * The scenery is drawn inline (SVG) rather than sourced from stock
 * imagery, so it always matches the AKAR TANI palette exactly.
 */
export function LandscapePanel({
  ranking,
  predSummary,
  loading,
}: {
  ranking: OrganicRanking[] | null
  predSummary: PredictionSummary[] | null
  loading: boolean
}) {
  const top = ranking?.[0]
  const lead = predSummary
    ?.slice()
    .sort((a, b) => b.total_prediksi - a.total_prediksi)[0]
  const totalPrediction =
    predSummary?.reduce((s, p) => s + p.total_prediksi, 0) ?? 0
  const materialCount = ranking?.length ?? 0

  return (
    <section className="landscape" aria-label="Ringkasan kontekstual AKAR TANI">
      <div className="landscape__sky" aria-hidden="true">
        <span className="landscape__sun" />
      </div>
      <LandscapeScene />

      <div className="landscape__body">
        <div className="landscape__ident">
          <img
            className="landscape__logo"
            src={LOGO_SRC}
            alt=""
            aria-hidden="true"
            width={46}
            height={46}
          />
          <div>
            <p className="landscape__name">AKAR TANI</p>
            <p className="landscape__desc">
              Sistem informasi &amp; pengembangan usaha pertanian Desa
              Cangkringan
            </p>
          </div>
        </div>

        {loading ? (
          <p className="landscape__meta">Memuat ringkasan…</p>
        ) : (
          <>
            {top && (
              <div className="landscape__block">
                <p className="landscape__label">
                  <BadgeCheck size={13} aria-hidden="true" /> Bahan organik
                  unggulan
                </p>
                <p className="landscape__value">{top.jenis_bahan_organik}</p>
                <p className="landscape__meta tnum">
                  Skor SAW {top.skor_akhir.toFixed(4)} · peringkat 1
                </p>
              </div>
            )}

            <div className="landscape__divider" />

            {lead && (
              <div className="landscape__block">
                <p className="landscape__label">
                  <Layers size={13} aria-hidden="true" /> Perkiraan produk
                  tertinggi 2026
                </p>
                <p className="landscape__value">{lead.produk}</p>
                <p className="landscape__meta tnum">
                  ± {formatNumber(Math.round(lead.total_prediksi))} unit
                </p>
              </div>
            )}

            {totalPrediction > 0 && (
              <div className="landscape__highlight">
                <span className="landscape__highlight-num tnum">
                  {formatNumber(Math.round(totalPrediction))}
                </span>
                <span className="landscape__highlight-label">
                  total perkiraan produksi pupuk 2026
                </span>
              </div>
            )}

            {materialCount > 0 && (
              <div className="landscape__block">
                <p className="landscape__label">
                  <MapPin size={13} aria-hidden="true" /> Cakupan analisis
                </p>
                <p className="landscape__meta">
                  {materialCount} jenis bahan organik dinilai dengan
                  pembobotan AHP &amp; skoring SAW.
                </p>
              </div>
            )}
          </>
        )}

        <p className="landscape__note">
          Angka prediksi berasal dari model machine learning yang telah
          dilatih — bukan jaminan permintaan.
        </p>
      </div>
    </section>
  )
}

/**
 * Stylised terraced-rice-field landscape. Drawn inline so it scales to
 * any panel height and stays on-palette.
 */
function LandscapeScene() {
  return (
    <svg
      className="landscape__scene"
      viewBox="0 0 336 300"
      preserveAspectRatio="xMidYMax slice"
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        <linearGradient id="at-hill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#2f7a52" />
          <stop offset="100%" stopColor="#1d4a3a" />
        </linearGradient>
        <linearGradient id="at-terrace-a" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#83c957" />
          <stop offset="100%" stopColor="#399b54" />
        </linearGradient>
        <linearGradient id="at-terrace-b" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#6fbf4d" />
          <stop offset="100%" stopColor="#2c7a45" />
        </linearGradient>
        <linearGradient id="at-water" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#bfe8f3" />
          <stop offset="100%" stopColor="#5cb8d0" />
        </linearGradient>
      </defs>

      {/* distant hills */}
      <path
        d="M0 150 L58 106 L104 140 L150 96 L210 146 L262 112 L336 156 L336 300 L0 300 Z"
        fill="url(#at-hill)"
        opacity="0.9"
      />
      <path
        d="M0 176 L70 142 L128 172 L196 134 L268 170 L336 146 L336 300 L0 300 Z"
        fill="#17453a"
      />

      {/* terraced rice fields, each tier sweeping across the panel */}
      <path
        d="M0 214 C70 196 130 208 200 198 C258 190 300 200 336 194 L336 232 C296 238 252 228 196 236 C132 246 66 236 0 252 Z"
        fill="url(#at-terrace-a)"
      />
      <path
        d="M0 252 C66 236 132 246 196 236 C252 228 296 238 336 232 L336 266 C288 272 246 262 190 270 C126 280 62 272 0 288 Z"
        fill="url(#at-terrace-b)"
      />

      {/* irrigation channel catching the sky */}
      <path
        d="M0 232 C70 218 140 228 210 218 C264 210 302 220 336 214 L336 224 C300 230 262 220 208 228 C138 238 70 228 0 242 Z"
        fill="url(#at-water)"
        opacity="0.55"
      />

      {/* foreground: saplings in a row, silhouetted */}
      <g fill="#123a30" opacity="0.92">
        <path d="M40 300 L40 258 M40 262 C30 260 24 252 24 246 C32 246 38 252 40 258 M40 266 C50 264 56 256 56 250 C48 250 42 256 40 262 Z" />
        <path d="M120 300 L120 250 M120 254 C109 252 103 244 103 237 C112 237 118 244 120 250 M120 258 C131 256 137 248 137 241 C128 241 122 248 120 254 Z" />
        <path d="M212 300 L212 256 M212 260 C201 258 195 250 195 243 C204 243 210 250 212 256 M212 264 C223 262 229 254 229 247 C220 247 214 254 212 260 Z" />
        <path d="M296 300 L296 252 M296 256 C285 254 279 246 279 239 C288 239 294 246 296 252 M296 260 C307 258 313 250 313 243 C304 243 298 250 296 256 Z" />
      </g>
    </svg>
  )
}
