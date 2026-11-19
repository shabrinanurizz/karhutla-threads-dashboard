"""Halaman Overview — fondasi dashboard sesuai referensi desain.

KPI dihitung dari data aktual (data/raw/comments_raw.csv dan
data/processed/comments_clean.csv). Teks judul, latar belakang, dan tujuan
masih berupa placeholder (berlabel jelas) dan akan diganti teks final.
"""

import streamlit as st

from src import config
from src.data_loader import load_raw_data, load_processed_data
from src.preprocessing import count_rows, count_unique, get_date_range
from src.visualization import (
    render_page_title,
    render_banner,
    render_kpi,
    render_section_header,
    render_process_flow,
    render_data_notice,
)

NAMA_BULAN = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


def _format_periode(lo, hi):
    """Rentang tanggal ke format '2-31 Agustus 2026' (jika bulan & tahun sama)."""
    if lo.year == hi.year and lo.month == hi.month:
        return f"{lo.day}-{hi.day} {NAMA_BULAN[lo.month]} {lo.year}"
    return f"{lo:%d-%m-%Y} s.d. {hi:%d-%m-%Y}"


def render():
    render_page_title(config.PROJECT_TITLE, accent=True)

    df_raw = load_raw_data()
    df_proc = load_processed_data()

    if df_raw is None or df_proc is None:
        render_data_notice(
            "Dataset belum tersedia di folder data/raw atau data/processed. "
            "Unggah file CSV terlebih dahulu agar KPI ditampilkan.",
            level="warning",
        )
        return

    n_raw = count_rows(df_raw)
    n_proc = count_rows(df_proc)
    n_user = count_unique(df_proc, config.COLUMNS["user"])
    periode = get_date_range(df_proc, config.COLUMNS["date"])

    # 4 KPI card (selaras referensi Overview).
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi(
            "Total Komentar Sebelum Pre-processing",
            n_raw,
            variant="dark",
            width="100%",
            height="130px",
            value_size="3rem",
            title_size="1rem",
            title_line_height="1.5",
            title_margin="3px",
            padding="12px 10px",
        )

    with col2:
        render_kpi(
            "Total Komentar Setelah Pre-processing",
            n_proc,
            variant="red",
            width="100%",
            height="130px",
            value_size="3rem",
            title_size="1rem",
            title_line_height="1.5",
            title_margin="3px",
            padding="12px 10px",
        )

    with col3:
        render_kpi(
            "Jumlah Pengguna Unik",
            n_user,
            variant="orange",
            width="100%",
            height="130px",
            value_size="3rem",
            title_size="1rem",
            title_line_height="1.5",
            title_margin="3px",
            padding="12px 10px",
        )

    with col4:
        render_kpi(
            "Periode Pengambilan Data",
            "13-08-2026\ns.d.\n12-11-2026",
            variant="dark",
            width="100%",
            height="130px",
            value_size="1.5rem",
            title_size="1rem",
            title_line_height="1.5",
            title_margin="3px",
            padding="12px 10px",
        )

    # Banner hijau: Latar Belakang dan Tujuan (placeholder teks).
    render_banner(
        ("LATAR BELAKANG", config.BACKGROUND_TEXT),
        ("TUJUAN", config.OBJECTIVE_TEXT),
    )

    # Panel alur manajemen dan analisis data (8 langkah).
    render_section_header("ALUR MANAJEMEN DAN ANALISIS DATA")
    render_process_flow(config.WORKFLOW_STEPS)


render()

