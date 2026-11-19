"""Halaman Topic Analysis / Modelling (Tahap 4 — diimplementasikan).

Integrasi dengan `src/topic_modeling.py` untuk pemodelan LDA dari data aktual
(`data/processed/comments_clean.csv`, kolom `text_clean`). Visualisasi
donut proporsi, line skor koherens, dan bar kata per topik ditampilkan
saat data tersedia, dan kembali ke placeholder saat belum tersedia.
"""

import streamlit as st

from src import config
from src.topic_modeling import (
    preprocess_texts,
    run_lda,
    coherence_scores,
    topic_proportion,
    top_words_per_topic,
)
from src.data_loader import load_processed_data
from src.visualization import (
    render_page_title,
    render_section_header,
    render_kpi,
    render_pill_label,
    render_placeholder_card,
    render_data_notice,
    render_donut_chart,
    render_line_chart,
    render_bar_chart,
)


def render():

    # ------------------------------------------------------------------
    # Load data
    # ------------------------------------------------------------------
    df = load_processed_data()
    if df is None:
        render_data_notice(
            "Dataset belum tersedia di folder data/processed. "
            "Unggah file CSV terlebih dahulu agar topic modelling dapat ditampilkan.",
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
    # Preprocessing + LDA
    # ------------------------------------------------------------------
    tokens = preprocess_texts(texts)
    n_topics = 4
    model, df_topik = run_lda(tokens, n_topics=n_topics)

    # ------------------------------------------------------------------
    # Baris pertama: donut proporsi + line skor koherens
    # ------------------------------------------------------------------
    col_a, col_b = st.columns(2)
    with col_a:
        render_section_header("Proporsi Komentar Per Topik")
        if model is not None:
            proporsi = topic_proportion(model, df)
            if proporsi is not None and len(proporsi) > 0:
                render_donut_chart(
                    proporsi,
                    names="topik",
                    values="proporsi",
                    title="Proporsi Komentar Per Topik",
                )
            else:
                render_placeholder_card(
                    "Proporsi Komentar Per Topik",
                    "Tidak dapat menghitung proporsi topik dari model LDA.",
                )
        else:
            render_placeholder_card(
                "Proporsi Komentar Per Topik",
                "Model LDA belum tersedia. Pastikan data komentar cukup "
                "dan coba jalankan ulang halaman ini.",
            )
    with col_b:
        render_section_header("Skor Koherens")
        if model is not None:
            models_range = []
            for k in range(2, 9):
                m_k, _ = run_lda(tokens, n_topics=k)
                if m_k is not None:
                    models_range.append((k, m_k))
            koherens_df = coherence_scores(models_range)
            if koherens_df is not None and len(koherens_df) > 0:
                render_line_chart(
                    koherens_df,
                    x="n_topik",
                    y="koherens",
                    title="Skor Koherens per Jumlah Topik",
                    markers=True,
                )
            else:
                render_placeholder_card(
                    "Skor Koherens",
                    "Tidak dapat menghitung skor koherens.",
                )
        else:
            render_placeholder_card(
                "Skor Koherens",
                "Model LDA belum tersedia untuk perhitungan skor koherens.",
            )

    st.divider()

    # ------------------------------------------------------------------
    # Pemilih topik A / B + tombol apply
    # ------------------------------------------------------------------
    render_section_header("Perbandingan Topik")
    topik_options = [f"Topik {i+1}" for i in range(n_topics)]
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.selectbox(
            "Topik A",
            options=topik_options,
            index=0,
            key="tp_topik_a"
        )
    with c2:
        st.selectbox(
            "Topik B",
            options=topik_options,
            index=1 if n_topics > 1 else 0,
            key="tp_topik_b"
        )
    with c3:
        st.write("")
        st.button("Apply", key="tp_apply", use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # KPI perbandingan Topik A vs Topik B
    # ------------------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    for kolom, label in zip(
        (k1, k2, k3, k4),
        ("Jumlah Komentar", "Rata-rata Likes", "Rata-rata Replies", "Rata-rata Shares"),
    ):
        with kolom:
            render_pill_label(label, variant="dark")
            c_a, c_b = st.columns(2)
            with c_a:
                topik_a = st.session_state.get("tp_topik_a", topik_options[0])
                count_a = int((df_topik["topik"] == topik_a).sum()) if df_topik is not None else 0
                render_kpi(topik_a, count_a, variant="dark", compact=True)
            with c_b:
                topik_b = st.session_state.get("tp_topik_b", topik_options[1] if len(topik_options) > 1 else topik_options[0])
                count_b = int((df_topik["topik"] == topik_b).sum()) if df_topik is not None else 0
                render_kpi(topik_b, count_b, variant="red", compact=True)

    st.divider()

    # ------------------------------------------------------------------
    # Top Kata Per Topik + Kontrol Model
    # ------------------------------------------------------------------
    col_c, col_d = st.columns([2, 1])
    with col_c:
        render_section_header("Top Kata Per Topik")
        if model is not None:
            top_words = top_words_per_topic(model, n=10)
            if top_words is not None and len(top_words) > 0:
                render_bar_chart(
                    top_words,
                    x="bobot",
                    y="kata",
                    title="Top Kata Per Topik",
                    horizontal=True,
                )
            else:
                render_placeholder_card(
                    "Top Kata Per Topik",
                    "Tidak dapat mengambil kata teratas per topik.",
                )
        else:
            render_placeholder_card(
                "Top Kata Per Topik",
                "Model LDA belum tersedia untuk menampilkan kata teratas.",
            )
    with col_d:
        render_section_header("Kontrol Model")
        st.slider("λ", 0.0, 1.0, 0.5, disabled=True, key="tp_lambda")
        render_kpi("Jumlah Topik", n_topics, variant="dark", compact=True)
        render_kpi("Total Dokumen", len(texts), variant="red", compact=True)

    render_data_notice(
        "Catatan: pemodelan topik dilakukan di `src/topic_modeling.py` "
        "menggunakan scikit-learn LDA pada dataset aktual dari "
        "`data/processed/comments_clean.csv`. Tidak ada hasil topik atau "
        "angka analisis yang dipersiapkan secara buatan.",
        level="info",
    )


render()

