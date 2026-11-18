"""Halaman Topic Modeling (kerangka Tahap 4 — BELUM diimplementasikan).

File ini menunjukkan bagaimana halaman akan terintegrasi dengan modul inti
ketika Tahap 4 dikerjakan. Tidak ada pemodelan, hasil topik, atau angka
analisis yang dipersiapkan di sini.

Alur integrasi yang direncanakan:

    # 1. Halaman memanggil fungsi pemodelan dari src/topic_modeling.py
    from src.topic_modeling import run_lda, coherence_scores, topic_proportion

    # 2. Fungsi-fungsi tersebut (harus dibuat di Tahap 4):
    #    - preprocess_texts(texts) -> list[list[str]]
    #    - run_lda(tokens, n_topics) -> model, topik_per_dokumen
    #    - coherence_scores(model_range) -> DataFrame(skor koherens per n_topik)
    #    - topic_proportion(model, df) -> DataFrame(proporsi komentar per topik)
    #    - top_words_per_topic(model, n) -> DataFrame(kata teratas per topik)

    # 3. Hasil dikirim ke komponen visualisasi bersama di src/visualization.py:
    #    - render_donut_chart(data, names="topik", values="proporsi", title=...)
    #    - render_line_chart(data, x="n_topik", y="koherens", title=...)
    #    - render_bar_chart(...)

Contoh fungsi stub ada di src/topic_modeling.py.
"""

import streamlit as st

from src import config
from src.visualization import (
    render_page_title,
    render_section_header,
    render_kpi,
    render_pill_label,
    render_placeholder_card,
    render_data_notice,
)


def render():
    render_page_title("PERBANDINGAN TOPIK")

    # ------------------------------------------------------------------
    # Baris pertama: donut proporsi + line skor koherens (placeholder)
    # ------------------------------------------------------------------
    col_a, col_b = st.columns(2)
    with col_a:
        render_section_header("Proporsi Komentar Per Topik")
        render_placeholder_card(
            "Proporsi Komentar Per Topik",
            "Donut chart proporsi komentar per topik dari hasil LDA. "
            "Dihasilkan oleh src.topic_modeling.topic_proportion dan "
            "divisualisasikan dengan src.visualization.render_donut_chart "
            "pada Tahap 4.",
        )
    with col_b:
        render_section_header("Skor Koherens (?)")
        render_placeholder_card(
            "Skor Koherens",
            "Line chart skor koherens untuk menentukan jumlah topik optimal. "
            "Dihasilkan oleh src.topic_modeling.coherence_scores dan "
            "divisualisasikan dengan src.visualization.render_line_chart "
            "pada Tahap 4.",
        )

    st.divider()

    # ------------------------------------------------------------------
    # Pemilih topik A / B + tombol apply (selaras referensi desain)
    # ------------------------------------------------------------------
    render_pill_label("Pemilih Topik", variant="dark")
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.text_input("Topik A", value="Topik 1", key="tp_topik_a")
    with c2:
        st.text_input("Topik B", value="Topik 2", key="tp_topik_b")
    with c3:
        st.write("")
        st.button("apply", key="tp_apply", use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # KPI perbandingan Topik A vs Topik B (placeholder)
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
                render_kpi("Topik 1", config.EMPTY_VALUE, variant="dark", compact=True)
            with c_b:
                render_kpi("Topik 2", config.EMPTY_VALUE, variant="red", compact=True)

    st.divider()

    # ------------------------------------------------------------------
    # Tren jumlah komentar per hari + kontrol model (placeholder)
    # ------------------------------------------------------------------
    col_c, col_d = st.columns([2, 1])
    with col_c:
        render_section_header("Tren Jumlah Komentar per hari")
        render_placeholder_card(
            "Tren Jumlah Komentar per hari",
            "Line chart tren komentar per hari per topik (hasil pemrosesan "
            "src.topic_modeling), divisualisasikan dengan "
            "src.visualization.render_line_chart pada Tahap 4.",
        )
    with col_d:
        render_placeholder_card(
            "Kontrol Model (λ)",
            "Slider lambda dan pemetaan top x kata per topik akan diatur di sini "
            "setelah src.topic_modeling diimplementasikan.",
        )
        st.slider("λ", 0.0, 1.0, 0.5, disabled=True, key="tp_lambda")
        render_kpi("top x kata topik A", config.EMPTY_VALUE, variant="dark", compact=True)
        render_kpi("top x kata topik B", config.EMPTY_VALUE, variant="red", compact=True)

    render_data_notice(
        "Catatan: halaman ini adalah kerangka sintaks dan petunjuk integrasi. "
        "Implementasi pemodelan topik ada di src/topic_modeling.py (Tahap 4). "
        "Tidak ada hasil topik atau angka analisis yang dipersiapkan di sini.",
        level="info",
    )


render()

