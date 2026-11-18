"""Modul topic modeling (kerangka Tahap 4 — BELUM diimplementasikan).

File ini berisi contoh kerangka sintaks dan komentar yang menjelaskan alur
preprocessing hingga pemodelan. Tidak ada pemodelan, hasil topik, atau angka
analisis yang dijalankan/dipersiapkan di sini.

Alur yang direncanakan:

    teks -> cleaning/case folding -> stopword removal -> stemming -> tokenisasi
        -> vektorisasi (CountVectorizer / TfidfVectorizer)
        -> LDA (n_topik) -> topik per dokumen
        -> proporsi komentar per topik & kata teratas per topik
        -> visualisasi melalui src.visualization (donut, line, bar)

Fungsi yang nantinya perlu dibuat di Tahap 4:

    def preprocess_texts(texts: List[str]) -> List[List[str]]
    # Input: daftar teks komentar. Output: daftar token per dokumen.

    def run_lda(tokens_per_doc: List[List[str]], n_topics: int):
    # Input: token per dokumen dan jumlah topik.
    # Output: model LDA dan topik yang diprediksi per dokumen.

    def coherence_scores(models_range) -> pd.DataFrame
    # Input: daftar model LDA dengan n_topik bervariasi.
    # Output: DataFrame kolom ['n_topik', 'koherens'] untuk line chart.

    def topic_proportion(model, df) -> pd.DataFrame
    # Input: model LDA dan DataFrame komentar.
    # Output: DataFrame kolom ['topik', 'proporsi'] untuk donut chart.

    def top_words_per_topic(model, n: int = 10) -> pd.DataFrame
    # Output: DataFrame kolom ['topik', 'kata', 'bobot'].

Integrasi di pages/4_Topic_Analysis.py:

    from src.topic_modeling import run_lda, coherence_scores, topic_proportion
    from src.visualization import render_donut_chart, render_line_chart

    proporsi = topic_proportion(model, df)
    render_donut_chart(proporsi, names="topik", values="proporsi", title=...)
"""

from typing import List, Optional, Tuple

import pandas as pd


def preprocess_texts(texts: List[str]) -> List[List[str]]:
    """Stub: cleansing hingga tokenisasi teks komentar."""
    return []


def run_lda(tokens_per_doc: List[List[str]], n_topics: int) -> Tuple[Optional[object], Optional[pd.DataFrame]]:
    """Stub: pelatihan model LDA.

    Returns:
        (model, topik_per_dokumen) atau (None, None) jika belum diimplementasi.
    """
    return None, None


def coherence_scores(models_range) -> Optional[pd.DataFrame]:
    """Stub: hitung skor koherens untuk berbagai jumlah topik."""
    return None


def topic_proportion(model, df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Stub: hitung proporsi komentar per topik."""
    return None


def top_words_per_topic(model, n: int = 10) -> Optional[pd.DataFrame]:
    """Stub: ambil n kata teratas dengan bobot tertinggi per topik."""
    return None

