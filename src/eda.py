"""Modul analisis EDA (kerangka Tahap 4 — BELUM diimplementasikan penuh).

Contoh fungsi di bawah menunjukkan pola pemisahan tugas:
- Logika perhitungan ada di sini (`src/eda.py`).
- Tampilan dashboard ada di `pages/2_EDA.py`.

Fungsi-fungsi berikut adalah STUB (kerangka sintaks dengan docstring).
Masukkan implementasi asli setelah struktur dataset diketahui dan dipastikan
tidak ada angka hasil analisis yang dipersiapkan secara buatan.
"""

from typing import Optional

import pandas as pd


def calculate_total_comments(df: Optional[pd.DataFrame]) -> Optional[int]:
    """Hitung total komentar.

    Args:
        df: DataFrame komentar. None jika data belum tersedia.

    Returns:
        Jumlah baris, atau None jika df None.
    """
    if df is None:
        return None
    return int(len(df))


def calculate_sentiment_distribution(df: Optional[pd.DataFrame]):
    """Contoh fungsi distribusi sentimen (hanya ilustrasi).

    Args:
        df: DataFrame yang memiliki kolom sentimen.

    Returns:
        DataFrame dengan kolom 'sentimen' dan 'jumlah', atau None jika
        kolom sentimen tidak tersedia / df None.

    Catatan:
        Nama kolom disesuaikan dengan dataset aktual di `src/config.py`.
    """
    if df is None:
        return None
    # Implementasi asli ditulis di Tahap 4 setelah kolom sentimen diketahui.
    return None


def calculate_average_metric(df: Optional[pd.DataFrame], column: str) -> Optional[float]:
    """Hitung rata-rata metrik numerik pada satu kolom.

    Args:
        df: DataFrame.
        column: Nama kolom numerik (mis. "likes").

    Returns:
        Rata-rata nilai, atau None jika df/kolom tidak tersedia.
    """
    if df is None or column not in df.columns:
        return None
    return float(df[column].mean())

