"""Halaman Comment Explorer (kerangka Tahap 4 — BELUM diimplementasikan).

File ini menunjukkan tata letak filter, ringkasan, dan tabel komentar sesuai
referensi. Logika filtering, pencarian, dan pagination akan ditempatkan di
src/comment_explorer.py pada Tahap 4. Tidak ada isi komentar yang dipersiapkan
secara buatan di sini.

Fungsi yang direncanakan di src/comment_explorer.py:

    def filter_comments(df, date_range=None, topic=None, query=None) -> DataFrame
    def summary_stats(df) -> dict  # total komentar, topik terbanyak, rata-rata likes
    def paginate(df, page, page_size) -> (DataFrame, total_pages)

Pemakaian di halaman (contoh integrasi):

    from src.comment_explorer import filter_comments, summary_stats, paginate
    from src.visualization import render_kpi

    df_view = filter_comments(df, date_range, topik, query)
    stats = summary_stats(df_view)
    render_kpi("Total komentar", stats["total"])
    ...

"""

import streamlit as st

from src import config
from src.visualization import (
    render_page_title,
    render_section_header,
    render_kpi,
    render_info_card,
    render_data_notice,
    render_badge,
    render_placeholder_card,
)


def render():
    render_page_title("COMMENT EXPLORER")

    # ------------------------------------------------------------------
    # Baris filter: Dari tanggal, Sampai tanggal, Topik, Cari Komentar, apply
    # ------------------------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns([1.6, 1.6, 1.6, 2.2, 0.9])
    with c1:
        st.date_input("Dari tanggal", key="ce_from", value=None)
    with c2:
        st.date_input("Sampai tanggal", key="ce_to", value=None)
    with c3:
        st.selectbox(
            "Topik",
            options=["Topik 1", "Topik 2", "Topik 3", "Topik 4"],
            index=None,
            placeholder="Pilih topik...",
            key="ce_topic",
        )
    with c4:
        st.text_input("Cari Komentar", placeholder="cari kata kunci...", key="ce_query")
    with c5:
        st.write("")
        st.button("apply", key="ce_apply", use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # Panel kiri: Ringkasan (placeholder metrics)
    # Panel kanan: Daftar Komentar (tabel placeholder)
    # ------------------------------------------------------------------
    col_left, col_right = st.columns([0.32, 0.68])

    with col_left:
        render_section_header("Ringkasan")
        render_info_card(
            "Total komentar",
            config.EMPTY_VALUE,
            variant="dark",
        )
        render_info_card("Topik terbanyak", config.EMPTY_VALUE, variant="dark")
        render_info_card("Rata-rata likes", config.EMPTY_VALUE, variant="dark")

    with col_right:
        render_section_header("Daftar Komentar")
        render_placeholder_card(
            "Daftar Komentar",
            "Tabel komentar (Tanggal | Topik | Komentar | Likes) dengan pagination "
            "akan ditampilkan di Tahap 4 setelah src.comment_explorer.py "
            "diimplementasikan.",
        )
        render_data_notice(
            "Contoh penanda topik pada tabel (badge) dihasilkan oleh "
            "render_badge dari src.visualization, mis. render_badge('Topik 1').",
            level="info",
        )

    render_data_notice(
        "Catatan: halaman ini adalah kerangka tampilan. Implementasi filtering, "
        "pencarian, dan pagination ada di src/comment_explorer.py (Tahap 4). "
        "Tidak ada isi komentar yang dipersiapkan secara buatan di sini.",
        level="info",
    )


render()

