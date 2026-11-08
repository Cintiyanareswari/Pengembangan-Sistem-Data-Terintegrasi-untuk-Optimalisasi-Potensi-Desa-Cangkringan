import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './styles/tokens.css'
import './styles/app.css'

import { AppLayout } from './components/AppLayout'
import { DashboardPage } from './pages/DashboardPage'
import { BahanOrganikPage } from './pages/BahanOrganikPage'
import { AnalisisPage } from './pages/AnalisisPage'
import { ProduksiPenjualanPage } from './pages/ProduksiPenjualanPage'
import { PrediksiPage } from './pages/PrediksiPage'
import { KatalogPage } from './pages/KatalogPage'
import { NotFoundPage } from './pages/NotFoundPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'bahan-organik', element: <BahanOrganikPage /> },
      { path: 'analisis', element: <AnalisisPage /> },
      { path: 'produksi-penjualan', element: <ProduksiPenjualanPage /> },
      { path: 'prediksi', element: <PrediksiPage /> },
      { path: 'katalog', element: <KatalogPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)