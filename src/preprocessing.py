"""Fungsi ringkasan data dasar yang tidak bergantung pada nama kolom tertentu.

Pipeline preprocessing teks (cleaning, stopword, stemming, tokenisasi) dikerjakan
di `notebooks/01_preprocessing.ipynb` setelah dataset tersedia; hasilnya disimpan
ke `data/processed/`.
"""

import pandas as pd

from src import config


def count_rows(df):
    """Jumlah baris DataFrame, atau None jika df None."""
    return None if df is None else int(len(df))


def count_unique(df, column):
    """Jumlah nilai unik pada `column`; None jika df/kolom tidak tersedia."""
    if df is None or not column or column not in df.columns:
        return None
    return int(df[column].nunique())


def get_date_range(df, column):
    """Kembalikan (tanggal_min, tanggal_maks) dari `column`; None jika tak tersedia."""
    if df is None or not column or column not in df.columns:
        return None
    dates = pd.to_datetime(df[column], errors="coerce").dropna()
    if dates.empty:
        return None
    return dates.min(), dates.max()
