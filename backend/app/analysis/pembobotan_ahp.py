
import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("storage/analysis")

# Urutan kriteria:
# C1 = Ketersediaan
# C2 = Kontinuitas
# C3 = Jarak
# C4 = Kemudahan pengumpulan

matriks = np.array([
    [1,   1/3, 3,   5],
    [3,   1,   5,   5],
    [1/3, 1/5, 1,   3],
    [1/5, 1/5, 1/3, 1]
], dtype=float)

kriteria = [
    "ketersediaan",
    "kontinuitas",
    "jarak",
    "kemudahan"
]


def main():
    # Menghitung eigenvalue dan eigenvector
    eigenvalues, eigenvectors = np.linalg.eig(matriks)

    index = np.argmax(eigenvalues.real)

    lambda_max = eigenvalues[index].real
    bobot = eigenvectors[:, index].real
    bobot = bobot / bobot.sum()

    # Menghitung konsistensi
    n = len(kriteria)
    CI = (lambda_max - n) / (n - 1)
    RI = 0.90
    CR = CI / RI

    # Menampilkan matriks
    print("=" * 45)
    print("PEMBOBOTAN AHP VINIX7")
    print("=" * 45)

    print("\nMatriks Perbandingan:")
    print(pd.DataFrame(
        matriks,
        index=kriteria,
        columns=kriteria
    ).round(3))

    # Menampilkan bobot
    hasil = pd.DataFrame({
        "kriteria": kriteria,
        "bobot": bobot
    })

    print("\nBobot Prioritas:")
    print(hasil.to_string(index=False))

    print("\nPengujian Konsistensi:")
    print(f"Lambda Max : {lambda_max:.4f}")
    print(f"CI         : {CI:.4f}")
    print(f"RI         : {RI:.2f}")
    print(f"CR         : {CR:.4f}")
    print(f"CR (%)     : {CR * 100:.2f}%")

    if CR <= 0.10:
        print("\nMatriks AHP KONSISTEN.")
    else:
        print("\nMatriks AHP BELUM KONSISTEN.")

    # Simpan hasil bobot
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hasil.to_csv(
        OUTPUT_DIR / "bobot_ahp.csv",
        index=False
    )

    print("\nBobot tersimpan di storage/analysis/bobot_ahp.csv")
    print("PEMBOBOTAN AHP SELESAI!")


if __name__ == "__main__":
    main()
