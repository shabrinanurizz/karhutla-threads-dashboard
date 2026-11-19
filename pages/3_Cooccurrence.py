"""Halaman Co-occurrence Analysis (Tahap 4 — diimplementasikan).

Integrasi dengan `src/cooccurrence.py` untuk perhitungan kemunculan bersama
kata dari data aktual (`data/processed/comments_clean.csv`, kolom `text_clean`).
Area visualisasi ditampilkan sebagai chart nyata saat data tersedia, dan
kembali ke placeholder saat data belum tersedia.
"""

import streamlit as st

from src import config
from src.cooccurrence import tokenize_texts, calculate_cooccurrence, get_top_pairs
from src.data_loader import load_processed_data
from src.visualization import (
    render_page_title,
    render_section_header,
    render_pill_label,
    render_placeholder_card,
    render_data_notice,
    render_badge,
    render_bar_chart,
    render_heatmap,
)


def render():
    render_page_title("CO- OCCURRENCE ANALYSIS")

    # ------------------------------------------------------------------
    # Load data
    # ------------------------------------------------------------------
    df = load_processed_data()
    if df is None:
        render_data_notice(
            "Dataset belum tersedia di folder data/processed. "
            "Unggah file CSV terlebih dahulu agar analisis co-occurrence dapat ditampilkan.",
            level="warning",
        )
        return

    text_col = config.COLUMNS["text_clean"]
    if text_col not in df.columns:
        render_data_notice(
            f"Kolom teks '{text_col}' tidak ditemukan dalam dataset.",
            level="warning",
        )
        return

    texts = df[text_col].dropna().astype(str).tolist()

    # ------------------------------------------------------------------
    # Filter: minimal kata muncul bersama + tombol apply
    # ------------------------------------------------------------------
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

    min_cooccur = st.session_state.get("co_min", 2)

    st.divider()

    # ------------------------------------------------------------------
    # Hitung co-occurrence
    # ------------------------------------------------------------------
    tokens = tokenize_texts(texts)
    co_df = calculate_cooccurrence(tokens, min_cooccur=min_cooccur)

    # ------------------------------------------------------------------
    # Area utama: jaringan kata (heatmap)
    # ------------------------------------------------------------------
    render_section_header("Co-occurrence Network")
    if co_df is not None and len(co_df) > 0:
        heat_df = co_df[["kata_a", "kata_b", "jumlah"]].copy()
        render_heatmap(
            heat_df,
            x="kata_a",
            y="kata_b",
            z="jumlah",
            title="Heatmap Co-occurrence Kata",
            height=400,
        )
    else:
        render_placeholder_card(
            "Jaringan Kata (Co-occurrence Network)",
            "Tidak ada pasangan kata yang memenuhi filter minimal "
            f"kemunculan bersama ({min_cooccur}x). Coba turunkan nilai filter.",
        )

    st.divider()

    # ------------------------------------------------------------------
    # Kolom kiri: Top 10 Pasangan Kata (bar chart)
    # Kolom kanan: Kata target filter + Network Kata Target
    # ------------------------------------------------------------------
    col_a, col_b = st.columns(2)
    with col_a:
        render_section_header("Top 10 Pasangan Kata")
        if co_df is not None and len(co_df) > 0:
            top_pairs = get_top_pairs(co_df, top_n=10)
            if top_pairs is not None and len(top_pairs) > 0:
                render_bar_chart(
                    top_pairs,
                    x="jumlah",
                    y="kata_a",
                    title="Top 10 Pasangan Kata",
                    horizontal=True,
                )
            else:
                render_placeholder_card(
                    "Top 10 Pasangan Kata",
                    "Tidak ada pasangan kata yang memenuhi filter.",
                )
        else:
            render_placeholder_card(
                "Top 10 Pasangan Kata",
                "Daftar pasangan kata dengan kemunculan bersama tertinggi akan "
                "ditampilkan sebagai bar chart horizontal setelah data tersedia.",
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
        kata_target = st.session_state.get("co_target", "").strip()
        if co_df is not None and len(co_df) > 0 and kata_target:
            target_pairs = get_top_pairs(co_df, top_n=10, keyword=kata_target)
            if target_pairs is not None and len(target_pairs) > 0:
                render_bar_chart(
                    target_pairs,
                    x="jumlah",
                    y="kata_a",
                    title=f"Network Kata: '{kata_target}'",
                    horizontal=True,
                )
            else:
                render_placeholder_card(
                    "Network Kata Target",
                    f"Tidak ada pasangan kata yang mengandung '{kata_target}'.",
                )
        else:
            render_placeholder_card(
                "Network Kata Target",
                "Masukkan kata target di kolom filter lalu klik apply "
                "untuk menampilkan sub-jaringan kata tersebut.",
            )

    render_data_notice(
        "Catatan: perhitungan co-occurrence dilakukan di `src/cooccurrence.py` "
        "menggunakan dataset aktual dari `data/processed/comments_clean.csv`. "
        "Tidak ada angka hasil analisis yang dipersiapkan secara buatan.",
        level="info",
    )


render()

