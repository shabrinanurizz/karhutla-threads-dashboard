"""Pemuatan dataset dengan path terpusat dan cache.

Tidak ada asumsi nama kolom di sini. Jika dataset belum ada, fungsi
mengembalikan None agar halaman dapat menampilkan pesan yang jelas.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from src import config

SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls")


def find_data_file(directory, filename=None):
    """Cari file dataset.

    Args:
        directory: Folder pencarian.
        filename: Nama file spesifik. Jika None, ambil file pertama yang didukung.

    Returns:
        Path file, atau None jika tidak ditemukan.
    """
    directory = Path(directory)
    if filename:
        candidate = directory / filename
        return candidate if candidate.is_file() else None
    if not directory.is_dir():
        return None
    files = sorted(p for p in directory.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    return files[0] if files else None


@st.cache_data(show_spinner="Memuat data...")
def _read_file(path_str, mtime):
    """Baca file (di-cache; `mtime` membuat cache refresh saat file berubah)."""
    path = Path(path_str)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def load_dataset(directory, filename=None):
    """Muat dataset dari folder. Return DataFrame, atau None jika belum tersedia/gagal dibaca."""
    path = find_data_file(directory, filename)
    if path is None:
        return None
    try:
        return _read_file(str(path), path.stat().st_mtime)
    except Exception as exc:  # file rusak, encoding, dll.
        st.error(f"Gagal membaca {path.name}: {exc}")
        return None


def load_raw_data():
    """Muat data mentah (sebelum preprocessing)."""
    return load_dataset(config.DATA_RAW_DIR, config.RAW_DATA_FILE)


def load_processed_data():
    """Muat data hasil preprocessing."""
    return load_dataset(config.DATA_PROCESSED_DIR, config.PROCESSED_DATA_FILE)
