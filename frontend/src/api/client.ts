// ============================================================
// VINIX7 — Centralized API client
// All backend calls go through here. Base URL from VITE_API_URL.
// ============================================================

import type {
  DashboardSummary,
  OrganicAnalysis,
  OrganicRanking,
  PredictionEntry,
  PredictionSummary,
  Product,
} from './types'

const BASE_URL = (import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000').replace(
  /\/+$/,
  '',
)

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { Accept: 'application/json' },
      signal,
    })
  } catch (err) {
    if ((err as Error).name === 'AbortError') throw err
    throw new ApiError(
      'Tidak dapat terhubung ke server AKAR TANI. Pastikan backend berjalan.',
      0,
    )
  }

  if (!res.ok) {
    let detail = `Permintaan gagal (${res.status})`
    try {
      const body = await res.json()
      if (body?.detail) detail = typeof body.detail === 'string' ? body.detail : detail
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(detail, res.status)
  }

  return (await res.json()) as T
}

export const api = {
  getDashboardSummary: (signal?: AbortSignal) =>
    request<DashboardSummary>('/dashboard/summary', signal),

  getOrganicAnalysis: (signal?: AbortSignal) =>
    request<OrganicAnalysis[]>('/organic/analysis', signal),

  getOrganicRanking: (signal?: AbortSignal) =>
    request<OrganicRanking[]>('/organic/ranking', signal),

  getPrediction2026: (signal?: AbortSignal) =>
    request<PredictionEntry[]>('/prediction/2026', signal),

  getPredictionSummary: (signal?: AbortSignal) =>
    request<PredictionSummary[]>('/prediction/summary', signal),

  getProducts: (signal?: AbortSignal) =>
    request<Product[]>('/catalog/products', signal),

  getProductById: (produkId: string, signal?: AbortSignal) =>
    request<Product>(`/catalog/products/${encodeURIComponent(produkId)}`, signal),
}