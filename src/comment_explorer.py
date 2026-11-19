"""Modul Comment Explorer (kerangka Tahap 4 — BELUM diimplementasikan penuh).

Logika filtering, pencarian, dan pagination ada di sini (`src/comment_explorer.py`).
Tampilan dashboard ada di `pages/5_Comment_Explorer.py`.

Fungsi-fungsi berikut adalah STUB. Implementasi asli ditulis di Tahap 4
sesuai struktur kolom dataset aktual (`src/config.py`). Tidak ada isi
komentar yang dipersiapkan secara buatan di sini.
"""

from typing import Optional, Tuple

import pandas as pd


def filter_comments(
    df: Optional[pd.DataFrame],
    date_range: Optional[Tuple[str, str]] = None,
    topic: Optional[str] = None,
    query: Optional[str] = None,
) -> Optional[pd.DataFrame]:
    """Filter komentar berdasarkan rentang tanggal, topik, dan pencarian teks.

    Args:
        df: DataFrame komentar asli.
        date_range: (tanggal_awal, tanggal_akhir) opsional.
        topic: Nilai topik yang difilter opsional.
        query: Kata kunci pencarian pada teks komentar opsional.

    Returns:
        DataFrame hasil filter, atau None jika df None.
    """
    if df is None:
        return None
    # Implementasi asli filtering ditulis di Tahap 4.
    return df


def summary_stats(df: Optional[pd.DataFrame]) -> dict:
    """Ringkasan statistik komentar untuk ditampilkan di panel kiri.

    Args:
        df: DataFrame komentar (sudah difilter).

    Returns:
        Dict dengan kunci: total, topik_terbanyak, rata_rata_likes.
        Semua nilai None jika data tidak tersedia.
    """
    return {
        "total": None,
        "topik_terbanyak": None,
        "rata_rata_likes": None,
    }


def paginate(
    df: Optional[pd.DataFrame], page: int = 1, page_size: int = 10
) -> Tuple[Optional[pd.DataFrame], int]:
    """Paginate DataFrame untuk tampilan tabel komentar.

    Args:
        df: DataFrame komentar.
        page: Halaman yang diminta (dimulai dari 1).
        page_size: Banyak baris per halaman.

    Returns:
        (DataFrame halaman ini, total halaman).
    """
    if df is None:
        return None, 0
    # Implementasi asli potongan data ditulis di Tahap 4.
    return df, 1

