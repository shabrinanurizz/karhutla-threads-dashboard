"""Halaman EDA — Exploratory Data Analysis.

Logika perhitungan ringkas ada di sini. Semua angka dihitung dari data
aktual (data/processed/comments_clean.csv); tidak ada angka dummy.
"""

import pandas as pd
import streamlit as st

from src import config
from src.data_loader import load_processed_data
from src.visualization import (
    render_page_title,
    render_section_header,
    render_kpi,
    render_pill_label,
    render_histogram,
    render_line_chart,
    render_heatmap,
    render_wordcloud,
    render_data_notice,
    render_placeholder_card,
)


def render():
    render_page_title("EXPLORATORY DATA ANALYSIS")

    df = load_processed_data()
    if df is None:
        render_data_notice(
            "Dataset hasil preprocessing belum tersedia di "
            f"{config.DATA_PROCESSED_DIR / config.PROCESSED_DATA_FILE}.",
            level="warning",
        )
        return

    date_col = config.COLUMNS["date"]
    text_col = config.COLUMNS["text"]

    # ------------------------------------------------------------------
    # KPI baris atas: Rata-rata Likes / Shares / Replies
    # ------------------------------------------------------------------
    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi("Rata-rata Likes", round(df[config.COLUMNS["likes"]].mean(), 2), variant="dark")
    with c2:
        render_kpi("Rata-rata Shares", round(df[config.COLUMNS["shares"]].mean(), 2), variant="red")
    with c3:
        render_kpi("Rata-rata Replies", round(df[config.COLUMNS["replies"]].mean(), 2), variant="orange")

    st.divider()

    # ------------------------------------------------------------------
    # Siapkan kolom turunan untuk chart (tanpa mengubah file asli)
    # ------------------------------------------------------------------
    df["_tanggal"] = pd.to_datetime(df[date_col], errors="coerce").dt.date
    df["_jam"] = pd.to_datetime(df[date_col], errors="coerce").dt.hour
    df["_hari"] = pd.to_datetime(df[date_col], errors="coerce").dt.day_name()
    df["_panjang"] = df[text_col].astype(str).str.len()

    # ------------------------------------------------------------------
    # Baris chart 2x2
    # ------------------------------------------------------------------
    row1a, row1b = st.columns(2)
    with row1a:
        render_section_header("WordCloud")
        render_wordcloud(df, text_col, title="WordCloud")
    with row1b:
        render_section_header("Distribusi Panjang Komentar")
        render_histogram(df, "_panjang", title="Distribusi panjang karakter komentar", nbins=30)

    row2a, row2b = st.columns(2)
    with row2a:
        render_section_header("Jumlah Komentar Per hari")
        harian = df.groupby("_tanggal").size().reset_index(name="jumlah")
        harian = harian.rename(columns={"_tanggal": "tanggal"})
        render_line_chart(harian, x="tanggal", y="jumlah", title="Tren jumlah komentar per hari")
    with row2b:
        render_section_header("Aktivitas Hari x Jam")
        aktivitas = (
            df.groupby(["_hari", "_jam"])
            .size()
            .reset_index(name="jumlah")
            .rename(columns={"_hari": "hari", "_jam": "jam", "jumlah": "jumlah"})
        )
        render_heatmap(aktivitas, x="jam", y="hari", z="jumlah", title="Heatmap aktivitas hari x jam")

    render_data_notice(
        "Catatan: kolom '_tanggal', '_jam', '_hari', dan '_panjang' adalah turunan "
        "untuk keperluan visualisasi ini dan tidak disimpan ke file asli.",
        level="info",
    )


render()

