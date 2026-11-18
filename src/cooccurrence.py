"""Modul analisis co-occurrence (kerangka Tahap 4 — BELUM diimplementasikan penuh).

Logika perhitungan kemunculan bersama kata ada di sini (`src/cooccurrence.py`).
Tampilan dashboard ada di `pages/3_Cooccurrence.py`.

Fungsi-fungsi berikut adalah STUB. Implementasi asli ditulis di Tahap 4
setelah dataset dan struktur kolom teks dipastikan. Tidak ada hasil
analisis yang dipersiapkan secara buatan di sini.
"""

from typing import Optional, List

import pandas as pd


def tokenize_texts(texts: List[str]) -> List[List[str]]:
    """Pisahkan teks menjadi daftar token per dokumen.

    Args:
        texts: Daftar string teks komentar.

    Returns:
        Daftar daftar token per dokumen.
    """
    # Implementasi asli (cleaning, stopword, stemming, tokenisasi) ditulis
    # di Tahap 4, merujuk hasil preprocessing di data/processed/.
    return [t.split() for t in texts]


def calculate_cooccurrence(
    tokens_per_doc: List[List[str]], min_cooccur: int = 2
) -> Optional[pd.DataFrame]:
    """Hitung kemunculan bersama pasangan kata dalam satu dokumen.

    Args:
        tokens_per_doc: Hasil tokenisasi per dokumen.
        min_cooccur: Minimal kemunculan bersama agar pasangan dicatat.

    Returns:
        DataFrame dengan kolom ['kata_a', 'kata_b', 'jumlah'], atau None jika
        input kosong.
    """
    if not tokens_per_doc:
        return None
    # Implementasi asli perhitungan pasangan kata ditulis di Tahap 4.
    return None


def get_top_pairs(
    cooccurrence_df: Optional[pd.DataFrame], top_n: int = 10, keyword: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """Ambil pasangan kata teratas, opsi difilter oleh kata target.

    Args:
        cooccurrence_df: Hasil calculate_cooccurrence.
        top_n: Banyak pasangan teratas.
        keyword: Jika diisi, hanya pasangan yang mengandung kata ini.

    Returns:
        DataFrame terurut menurun, atau None jika tidak ada data.
    """
    if cooccurrence_df is None or len(cooccurrence_df) == 0:
        return None
    # Implementasi asli filtering dan pengurutan ditulis di Tahap 4.
    return None

