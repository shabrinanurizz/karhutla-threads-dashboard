"""Halaman Co-occurrence Analysis (kerangka Tahap 4).

Tampilan siap untuk integrasi dengan `src/cooccurrence.py`. Saat ini area
visualisasi berupa placeholder dengan pesan yang jelas; tidak ada angka
hasil analisis yang dipersiapkan secara buatan.
"""

import streamlit as st

from src import config
from src.visualization import (
    render_page_title,
    render_section_header,
    render_pill_label,
    render_placeholder_card,
    render_data_notice,
    render_badge,
)


def render():
    render_page_title("CO- OCCURRENCE ANALYSIS")

    # ------------------------------------------------------------------
    # Filter: minimal kata muncul bersama + tombol apply
    # ------------------------------------------------------------------
    render_pill_label("Filter", variant="dark")
    col_f1, col_f2, col_f3 = st.columns([3, 1, 6])
    with col_f1:
        min_cooccur = st.number_input(
            "Minimal kata muncul bersama", min_value=1, value=2, step=1, key="co_min"
        )
    with col_f2:
        st.write("")
        apply_filter = st.button("apply", key="co_apply", use_container_width=True)
    with col_f3:
        st.write("")
    if apply_filter:
        st.session_state["co_min"] = min_cooccur
        st.success(f"Filter diterapkan: minimal {min_cooccur} kemunculan bersama.")

    st.divider()

    # ------------------------------------------------------------------
    # Area utama: jaringan kata (placeholder)
    # ------------------------------------------------------------------
    render_placeholder_card(
        "Jaringan Kata (Co-occurrence Network)",
        "Visualisasi jaringan akan ditampilkan di Tahap 4 setelah fungsi "
        "`src/cooccurrence.py` diimplementasikan dengan dataset aktual.",
    )

    st.divider()

    # ------------------------------------------------------------------
    # Kolom kiri: Top 10 Pasangan Kata (placeholder)
    # Kolom kanan: Kata target filter + Network Kata Target (placeholder)
    # ------------------------------------------------------------------
    col_a, col_b = st.columns(2)
    with col_a:
        render_section_header("Top 10 Pasangan Kata")
        render_placeholder_card(
            "Top 10 Pasangan Kata",
            "Daftar pasangan kata dengan kemunculan bersama tertinggi akan "
            "ditampilkan sebagai bar chart horizontal di Tahap 4.",
        )
    with col_b:
        render_pill_label("Kata target", variant="dark")
        col_t1, col_t2, col_t3 = st.columns([3, 1, 6])
        with col_t1:
            st.text_input("filter", placeholder="masukkan kata...", key="co_target")
        with col_t2:
            st.write("")
            st.button("apply", key="co_target_apply", use_container_width=True)
        with col_t3:
            st.write("")
        render_section_header("Network Kata Target")
        render_placeholder_card(
            "Network Kata Target",
            "Sub-jaringan untuk kata target yang dipilih akan ditampilkan di Tahap 4.",
        )

    render_data_notice(
        "Catatan: semua area di halaman ini adalah kerangka (placeholder). "
        "Implementasi perhitungan co-occurrence dilakukan di `src/cooccurrence.py` "
        "pada Tahap 4 dengan dataset aktual yang Anda berikan.",
        level="info",
    )


render()

