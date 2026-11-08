import type { OrganicRanking } from '../../api/types'
import { formatScore } from '../../utils/format'

/**
 * Ranked organic-material list with an inline SAW score bar.
 * Reused on the dashboard (top 5) and the analysis page (full list).
 */
export function RankingList({
  data,
  limit,
}: {
  data: OrganicRanking[]
  limit?: number
}) {
  const rows = limit ? data.slice(0, limit) : data

  if (rows.length === 0) return null

  // Normalize against the top score (typically ~1.0) so bars share one scale.
  const max = Math.max(...rows.map((r) => r.skor_akhir), 0.001)

  return (
    <ol className="ranking">
      {rows.map((r) => {
        const width = Math.max((r.skor_akhir / max) * 100, 4)
        return (
          <li key={r.peringkat} className="ranking__row">
            <span className="ranking__rank tnum">{r.peringkat}</span>
            <div className="ranking__body">
              <div className="ranking__meta">
                <span className="ranking__name">{r.jenis_bahan_organik}</span>
                <span className="ranking__score tnum">
                  {formatScore(r.skor_akhir)}
                </span>
              </div>
              <div
                className="ranking__track"
                role="img"
                aria-label={`Skor ${formatScore(r.skor_akhir)}`}
              >
                <div className="ranking__fill" style={{ width: `${width}%` }} />
              </div>
            </div>
          </li>
        )
      })}
    </ol>
  )
}