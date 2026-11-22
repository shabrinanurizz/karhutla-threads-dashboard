
"""Halaman Exploratory Data Analysis."""

import streamlit as st
from wordcloud import WordCloud

from src import config
from src.data_loader import load_processed_data, load_dataset
from src.eda import (
    calculate_average_metric,
    prepare_daily_comments,
    prepare_hourly_activity,
    prepare_comment_length,
    prepare_wordcloud_data,
)
from src.visualization import (
    render_page_title,
    render_kpi,
    render_histogram,
    render_line_chart,
    render_heatmap,
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
        width=500,
        height=190,
        background_color="#F8F5EC",
        color_func=color_word,
        max_words=65,
        prefer_horizontal=0.9,
        relative_scaling=0.5,
        min_font_size=7,
        margin=2,
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

    # CSS tampilan dashboard
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0.2rem !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.35rem;
    }

    .page-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        margin-top: 0 !important;
        margin-bottom: 0.2rem !important;
    }

    /* Border seluruh kartu visualisasi */
    div[data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stVerticalBlockBorderWrapper"] .st-emotion-cache-s5u6nk {
        border: 2px solid #1B4332 !important;
        border-radius: 12px !important;
        background: transparent !important;
    }

    /* Judul WordCloud */
    .eda-card-title {
        font-family: inherit;
        font-size: 18px;
        font-weight: 700;
        color: #1B4332;
        margin: 0;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Memuat data
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

    # 1. KPI Engagement
    st.markdown(
        '<div style="height: 10px;"></div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        value = calculate_average_metric(
            df, config.COLUMNS["likes"]
        )
        render_kpi(
            "Rata-rata Likes",
            round(value, 2) if value is not None else "—",
            variant="dark",
            compact=True,
            value_size="2rem",
            title_size="0.85rem",
            padding="7px 8px",
            title_margin="2px",
        )

    with c2:
        value = calculate_average_metric(
            df, config.COLUMNS["shares"]
        )
        render_kpi(
            "Rata-rata Shares",
            round(value, 2) if value is not None else "—",
            variant="red",
            compact=True,
            value_size="2rem",
            title_size="0.85rem",
            padding="7px 8px",
            title_margin="2px",
        )

    with c3:
        value = calculate_average_metric(
            df, config.COLUMNS["replies"]
        )
        render_kpi(
            "Rata-rata Replies",
            round(value, 2) if value is not None else "—",
            variant="orange",
            compact=True,
            value_size="2rem",
            title_size="0.85rem",
            padding="7px 8px",
            title_margin="2px",
        )

    # 2. Persiapan data
    daily = prepare_daily_comments(df)
    activity = prepare_hourly_activity(df)
    comment_length = prepare_comment_length(df)
    wordcloud_data = prepare_wordcloud_data(token_df)

    # 3. WordCloud dan Histogram
    col1, col2 = st.columns(2, gap="small")

    with col1:
        with st.container(border=True, height=360):
            st.markdown(
                '<div class="eda-card-title">WordCloud Komentar</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div style="height: 25px;"></div>',
                unsafe_allow_html=True,
            )

            render_wordcloud(wordcloud_data)

    with col2:
        with st.container(border=True, height=360):
            st.markdown(
                '<div style="height: 10px;"></div>',
                unsafe_allow_html=True,
            )

            render_histogram(
                comment_length,
                x="jumlah_kata",
                title="Distribusi Panjang Komentar (Jumlah Kata)",
                nbins=30,
                height=280,
                key="eda_comment_length",
            )

    # 4. Tren Harian dan Heatmap
    col1, col2 = st.columns(2, gap="small")

    with col1:
        with st.container(border=True, height=310):
            render_line_chart(
                daily,
                x="tanggal",
                y="jumlah",
                title="Tren Jumlah Komentar per Hari",
                height=250,
                key="eda_daily_comments",
            )

    with col2:
        with st.container(border=True, height=310):
            render_heatmap(
                activity,
                x="jam",
                y="hari",
                z="jumlah",
                title="Aktivitas Komentar berdasarkan Hari dan Jam",
                height=250,
                key="eda_hourly_activity",
            )


render()
