
"""Halaman Exploratory Data Analysis."""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re
import html
import xml.etree.ElementTree as ET
from wordcloud import WordCloud

from src import config
from src.data_loader import load_processed_data, load_dataset
from src.eda import (
    calculate_average_metric,
    calculate_total_comments,
    prepare_daily_comments,
    prepare_hourly_activity,
    prepare_comment_length,
    prepare_wordcloud_data,
)
from src.visualization import (
    render_page_title,
    render_section_header,
    render_kpi,
    render_histogram,
    render_line_chart,
    render_heatmap,
    render_bar_chart,
    render_data_notice,
)


def render_wordcloud(data):
    if data.empty:
        st.info("Data WordCloud belum tersedia.")
        return

    frequencies = dict(
        zip(data["kata"], data["frekuensi"])
    )

    palette = [
        "#E85D04",
        "#F48C06",
        "#1B4332",
        "#6C757D",
        "#9C6644",
        "#D97706",
    ]

    def color_word(word, **kwargs):
        return palette[
            sum(ord(char) for char in word) % len(palette)
        ]

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="#F8F5EC",
        color_func=color_word,
        max_words=100,
        prefer_horizontal=0.9,
        relative_scaling=0.5,
        min_font_size=8,
        margin=3,
        random_state=42,
    ).generate_from_frequencies(frequencies)

    st.image(
        wc.to_array(),
        use_container_width=True,
    )

    selected_word = st.selectbox(
        "Cari kata untuk melihat jumlah komentar:",
        options=data["kata"].tolist(),
        index=None,
        placeholder="Pilih kata...",
    )

    if selected_word:
        count = data.loc[
            data["kata"] == selected_word,
            "jumlah_komentar"
        ].iloc[0]

        st.success(
            f"Kata **'{selected_word}'** ditemukan dalam "
            f"**{count:,} komentar**."
        )


def render():

    render_page_title("EXPLORATORY DATA ANALYSIS")

    # CSS CARD
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFEFA !important;
        border: 2px solid #1B4332 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18) !important;
        padding: 18px !important;
        transition: box-shadow 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 12px 26px rgba(0, 0, 0, 0.23) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    df = load_processed_data()
    token_df = load_dataset(
        config.DATA_PROCESSED_DIR,
        "comments_tokenized.csv",
    )

    if df is None or df.empty:
        render_data_notice(
            "Dataset hasil preprocessing belum tersedia.",
            level="warning",
        )
        return

    # ---------------------------------------------------------
    # 1. Ringkasan Engagement
    # ---------------------------------------------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        value = calculate_average_metric(
            df, config.COLUMNS["likes"]
        )
        render_kpi(
            "Rata-rata Likes",
            round(value, 2) if value is not None else "—",
            variant="dark",
        )

    with c2:
        value = calculate_average_metric(
            df, config.COLUMNS["shares"]
        )
        render_kpi(
            "Rata-rata Shares",
            round(value, 2) if value is not None else "—",
            variant="red",
        )

    with c3:
        value = calculate_average_metric(
            df, config.COLUMNS["replies"]
        )
        render_kpi(
            "Rata-rata Replies",
            round(value, 2) if value is not None else "—",
            variant="orange",
        )

    # ---------------------------------------------------------
    # 2. Persiapan data
    # ---------------------------------------------------------
    daily = prepare_daily_comments(df)
    activity = prepare_hourly_activity(df)
    comment_length = prepare_comment_length(df)
    wordcloud_data = prepare_wordcloud_data(token_df)

    # ---------------------------------------------------------
    # 3. WordCloud dan Histogram
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True, height="stretch"):
            st.markdown("**WordCloud Komentar**")
            render_wordcloud(wordcloud_data)

    with col2:
        with st.container(border=True, height="stretch"):
            render_histogram(
                comment_length,
                x="jumlah_kata",
                title="Distribusi Panjang Komentar (Jumlah Kata)",
                nbins=30,
                key="eda_comment_length",
            )

    # ---------------------------------------------------------
    # 4. Tren Harian dan Heatmap
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True, height="stretch"):
            render_line_chart(
                daily,
                x="tanggal",
                y="jumlah",
                title="Tren Jumlah Komentar per Hari",
                key="eda_daily_comments",
            )

    with col2:
        with st.container(border=True, height="stretch"):
            render_heatmap(
                activity,
                x="jam",
                y="hari",
                z="jumlah",
                title="Aktivitas Komentar berdasarkan Hari dan Jam",
                key="eda_hourly_activity",
            )


render()
