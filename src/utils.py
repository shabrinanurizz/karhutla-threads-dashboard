"""Utility umum yang dipakai lintas halaman."""

from pathlib import Path

import streamlit as st

from src import config


def load_css(css_path=None):
    """Muat file CSS global (dan font) ke halaman Streamlit.

    Args:
        css_path: Path CSS. Default `config.CSS_PATH`.
    """
    path = Path(css_path) if css_path else config.CSS_PATH
    if not check_file_exists(path):
        st.warning(f"File CSS tidak ditemukan: {path}")
        return
    css = path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>@import url('{config.FONT_URL}');\n{css}</style>",
        unsafe_allow_html=True,
    )


def format_number(value):
    """Format angka dengan pemisah ribuan titik (gaya Indonesia). None -> "—"."""
    if value is None:
        return config.EMPTY_VALUE
    try:
        number = float(value)
        if number == int(number):
            return f"{int(number):,}".replace(",", ".")
        return f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return str(value)


def format_percentage(value, decimals=1):
    """Format rasio 0-1 menjadi persen, mis. 0.256 -> "25,6%". None -> "—"."""
    if value is None:
        return config.EMPTY_VALUE
    try:
        return f"{float(value) * 100:.{decimals}f}%".replace(".", ",")
    except (TypeError, ValueError):
        return str(value)


def check_file_exists(path):
    """Kembalikan True jika `path` ada dan berupa file."""
    if path is None:
        return False
    return Path(path).is_file()

