
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes import (
    dashboard,
    organic,
    prediction,
    catalog
)


app = FastAPI(
    title="VINIX7 API",
    description=(
        "API Sistem Informasi Terintegrasi "
        "Desa Cangkringan"
    ),
    version="1.0.0"
)


# Mengizinkan frontend (origin terpisah) mengakses API.
# Perubahan aditif — tidak mengubah route, schema, service, maupun kontrak API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://pengembangan-sistem-data-terintegrasi-w7ky.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Menghubungkan seluruh router
app.include_router(dashboard.router)
app.include_router(organic.router)
app.include_router(prediction.router)
app.include_router(catalog.router)


@app.get("/")
def root():
    return {
        "message": "VINIX7 API berhasil dijalankan",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "VINIX7 API"
    }
