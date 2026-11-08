/**
 * Maps catalog records to the product photographs shipped in
 * /public/assets/products.
 *
 * Why a manual map instead of using `foto_produk` directly:
 * the database column stores generic labels ("Foto Produk 1"), not
 * filenames, and the label order does not match the file order —
 * e.g. PRD-003 carries "Foto Produk 11" and PRD-004's asset is spelled
 * `commpossap.jpg`. The backend is intentionally left untouched, so the
 * translation lives here.
 *
 * Keying by produk_id is the stable contract; the product name is only a
 * secondary fallback in case IDs are ever reissued.
 */

const BY_ID: Record<string, string> = {
  'PRD-001': 'proquatic.jpg',
  'PRD-002': 'propunic.jpg',
  'PRD-003': 'profeed.jpg',
  'PRD-004': 'commpossap.jpg',
  'PRD-005': 'tricogem.jpg',
  'PRD-006': 'pendawa-subur-pertumbuhan.jpg',
  'PRD-007': 'beva-gem.jpg',
  'PRD-008': 'metha-gem.jpg',
  'PRD-009': 'pendawa-ampuh.jpg',
  'PRD-010': 'pendawa-subur-pembungaan.jpg',
  'PRD-011': 'pendawa-subur-tunas.jpg',
}

/** Normalised product-name → file, for resilience against ID changes. */
const BY_NAME: Record<string, string> = {
  proquatic: 'proquatic.jpg',
  propunic: 'propunic.jpg',
  profeed: 'profeed.jpg',
  compossap: 'commpossap.jpg',
  tricogem: 'tricogem.jpg',
  'pendawa subur pertumbuhan': 'pendawa-subur-pertumbuhan.jpg',
  'beva gem': 'beva-gem.jpg',
  'metha gem': 'metha-gem.jpg',
  'pendawa ampuh': 'pendawa-ampuh.jpg',
  pestisidaorganikpendawaampuh: 'pendawa-ampuh.jpg',
  'pendawa subur pembungaan': 'pendawa-subur-pembungaan.jpg',
  pendawasuburpembungaan: 'pendawa-subur-pembungaan.jpg',
  'pendawa subur tunas': 'pendawa-subur-tunas.jpg',
}

function normalize(name: string): string {
  return name
    .toLowerCase()
    .replace(/\(zpt\)/g, '')
    .replace(/organik/g, '')
    .replace(/[^a-z0-9 ]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

/**
 * Returns the public URL of a product photograph, or null when no asset
 * is known (callers then render the designed fallback).
 */
export function productPhotoUrl(
  produkId: string,
  namaProduk: string,
): string | null {
  const file = BY_ID[produkId] ?? BY_NAME[normalize(namaProduk)]
  return file ? `/assets/products/${file}` : null
}
