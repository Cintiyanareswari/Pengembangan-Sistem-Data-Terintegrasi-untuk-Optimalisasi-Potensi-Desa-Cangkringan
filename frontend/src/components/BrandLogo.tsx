/**
 * AKAR TANI brand lockup.
 * Uses the official logo asset (farmer + seedling + sack) provided in
 * /public/assets. Rendered as a small rounded tile so the logo keeps its
 * own white ground and stays crisp on both the white sidebar and the
 * dark landscape panel.
 */

export const LOGO_SRC = '/assets/logo-akar-tani.png'

export function BrandLogo() {
  return (
    <div className="brand">
      <img
        className="brand__logo"
        src={LOGO_SRC}
        alt="Logo AKAR TANI"
        width={46}
        height={46}
      />
      <span className="brand__text">
        <span className="brand__name">AKAR TANI</span>
        <span className="brand__sub">Desa Cangkringan</span>
      </span>
    </div>
  )
}
