
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_api_backend():

    print("\n=== PENGUJIAN API VINIX7 ===")

    # 1. Menguji halaman utama
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    print("Root endpoint: BERHASIL")

    # 2. Menguji health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("Health endpoint: BERHASIL")

    # 3. Menguji dashboard
    response = client.get("/dashboard/summary")
    assert response.status_code == 200

    dashboard = response.json()
    assert dashboard["total_produk"] == 11
    assert dashboard["total_data_penjualan"] == 792
    print("Dashboard endpoint: BERHASIL")

    # 4. Menguji analisis organik
    response = client.get("/organic/analysis")
    assert response.status_code == 200
    assert len(response.json()) == 88
    print("Organic analysis: BERHASIL")

    # 5. Menguji ranking organik
    response = client.get("/organic/ranking")
    assert response.status_code == 200

    ranking = response.json()
    assert len(ranking) == 17
    assert ranking[0]["peringkat"] == 1
    print("Organic ranking: BERHASIL")

    # 6. Menguji prediksi tahun 2026
    response = client.get("/prediction/2026")
    assert response.status_code == 200
    assert len(response.json()) == 132
    print("Prediction 2026: BERHASIL")

    # 7. Menguji ringkasan prediksi
    response = client.get("/prediction/summary")
    assert response.status_code == 200
    assert len(response.json()) == 11
    print("Prediction summary: BERHASIL")

    # 8. Menguji katalog produk
    response = client.get("/catalog/products")
    assert response.status_code == 200
    assert len(response.json()) == 11
    print("Catalog products: BERHASIL")

    # 9. Menguji detail produk
    response = client.get("/catalog/products/PRD-005")
    assert response.status_code == 200
    assert response.json()["nama_produk"] == (
        "Tricogem Fungisida Organik"
    )
    print("Catalog product detail: BERHASIL")

    # 10. Menguji produk yang tidak ditemukan
    response = client.get(
        "/catalog/products/ID-TIDAK-ADA"
    )
    assert response.status_code == 404
    print("Catalog HTTP 404: BERHASIL")

    print("\nSEMUA PENGUJIAN API BERHASIL!")


if __name__ == "__main__":
    test_api_backend()
