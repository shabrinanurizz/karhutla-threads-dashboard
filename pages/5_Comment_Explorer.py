"""Halaman Comment Explorer (Tahap 4)."""

import pandas as pd
import streamlit as st

from src import config
from src.comment_explorer import _get_col, filter_comments, paginate, summary_stats
from src.data_loader import load_dataset, load_processed_data, load_raw_data
from src.visualization import (
    render_data_notice,
    render_page_title,
    render_section_header,
)

TOPIC_COL_CANDIDATES = (
    "topic_label",
    "topik",
    "topic",
    "dominant_topic",
    "lda_topic",
    "topic_id",
    "cluster",
)


def _render_summary_card(label: str, value: str):
    """Render kartu ringkasan horizontal dengan latar hijau tua agar kontras dan proporsional."""
    st.markdown(
        f"""
        <div style="
            background-color: {config.COLORS['green_dark']};
            color: {config.COLORS['text_light']};
            padding: 14px 18px;
            border-radius: {config.LAYOUT['card_radius']};
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            font-family: '{config.FONT_FAMILY}', sans-serif;
            min-height: 88px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 0.82rem; font-weight: 600; opacity: 0.9; margin-bottom: 4px;">
                {label}
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; line-height: 1.25;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _format_topic_series(series: pd.Series) -> pd.Series:
    """Pertahankan label nama topik dari Modelling; rapikan jika masih berupa angka."""
    def _clean_val(val):
        if pd.isna(val):
            return pd.NA
        s = str(val).strip()
        if s == "" or s.lower() in ("nan", "none", config.EMPTY_VALUE):
            return pd.NA
        try:
            num_float = float(s)
            if num_float.is_integer():
                num = int(num_float)
                return f"Topik {num + 1}" if num >= 0 else s
        except ValueError:
            pass
        return s

    return series.apply(_clean_val)


def _find_populated_topic_col(df: pd.DataFrame) -> str | None:
    """Cari kolom topik yang benar-benar berisi data."""
    for col in TOPIC_COL_CANDIDATES:
        if col in df.columns and df[col].dropna().astype(str).str.strip().ne("").any():
            return col
    return _get_col(df, "topic", TOPIC_COL_CANDIDATES)


def _load_explorer_data() -> pd.DataFrame | None:
    """Memuat dataset komentar dan menyinkronkan kolom topik untuk filter & ringkasan."""
    df = load_processed_data()
    if df is None:
        df = load_raw_data()
    if df is None:
        return None

    df = df.copy()
    topic_col = _find_populated_topic_col(df)

    # Cek folder data/model_output jika kolom topik belum ada di dataset utama
    if topic_col is None:
        df_model = load_dataset(config.MODEL_OUTPUT_DIR)
        if df_model is not None:
            model_topic_col = _find_populated_topic_col(df_model)
            id_col = config.COLUMNS.get("id", "comment_id")
            if model_topic_col is not None:
                if id_col in df.columns and id_col in df_model.columns:
                    df = df.merge(
                        df_model[[id_col, model_topic_col]],
                        on=id_col,
                        how="left",
                    )
                elif len(df) == len(df_model):
                    df[model_topic_col] = df_model[model_topic_col].values

    topic_col = _find_populated_topic_col(df)
    if topic_col is not None:
        formatted = _format_topic_series(df[topic_col])
        df[topic_col] = formatted
        # Sinkronkan ke nama kolom standar agar filter_comments() dan summary_stats() membacanya
        std_topic_col = config.COLUMNS.get("topic", "topic")
        df[std_topic_col] = formatted
        df["topic"] = formatted

    return df


def render():
    render_page_title("COMMENT EXPLORER")

    df = _load_explorer_data()

    topic_options = [
        "Kritik ke Pemerintah dan Perusahaan",
        "Kondisi Kebakaran dan Lapangan",
        "Doa dan Kecaman Pembakaran",
        "Dampak Bencana dan Peran Sawit",
    ]
    topic_col = None
    if df is not None:
        topic_col = _find_populated_topic_col(df)
        if topic_col is not None:
            unique_topics = sorted(
                df[topic_col]
                .dropna()
                .astype(str)
                .str.strip()
                .loc[lambda s: (s != "") & (s != config.EMPTY_VALUE)]
                .unique()
                .tolist()
            )
            if unique_topics:
                topic_options = unique_topics

    # ------------------------------------------------------------------
    # Baris 1: Filter (Dari tanggal, Sampai tanggal, Topik, Cari Komentar, apply)
    # ------------------------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns([1.35, 1.35, 1.85, 2.05, 1.0])
    with c1:
        date_from = st.date_input("Dari tanggal", key="ce_from", value=None)
    with c2:
        date_to = st.date_input("Sampai tanggal", key="ce_to", value=None)
    with c3:
        selected_topic = st.selectbox(
            "Topik",
            options=topic_options,
            index=None,
            placeholder="Pilih topik...",
            key="ce_topic",
        )
    with c4:
        search_query = st.text_input(
            "Cari Komentar", placeholder="cari kata kunci...", key="ce_query"
        )
    with c5:
        st.write("")
        if st.button("apply", key="ce_apply", use_container_width=True):
            st.session_state["ce_page"] = 1

    # Terapkan filter & pastikan filter topik ikut menyaring baris tabel
    df_filtered = filter_comments(
        df,
        date_range=(date_from, date_to),
        topic=selected_topic,
        query=search_query,
    )
    if (
        df_filtered is not None
        and selected_topic
        and topic_col
        and topic_col in df_filtered.columns
    ):
        df_filtered = df_filtered[
            df_filtered[topic_col].fillna("").astype(str).str.strip()
            == str(selected_topic).strip()
        ]

    stats = summary_stats(df_filtered)

    # ------------------------------------------------------------------
    # Baris 2: Ringkasan (3 kartu berjejer ke samping di atas tabel)
    # ------------------------------------------------------------------
    render_section_header("Ringkasan")
    total_val = f"{stats['total']:,}" if stats["total"] is not None else config.EMPTY_VALUE
    top_topic_val = (
        str(stats["topik_terbanyak"])
        if stats["topik_terbanyak"] is not None
        else config.EMPTY_VALUE
    )
    avg_likes_val = (
        f"{stats['rata_rata_likes']:.1f}"
        if stats["rata_rata_likes"] is not None
        else config.EMPTY_VALUE
    )

    s1, s2, s3 = st.columns([1, 1.6, 1], gap="medium")
    with s1:
        _render_summary_card("Total komentar", total_val)
    with s2:
        _render_summary_card("Topik terbanyak", top_topic_val)
    with s3:
        _render_summary_card("Rata-rata likes", avg_likes_val)

    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Baris 3: Daftar Komentar
    # ------------------------------------------------------------------
    render_section_header("Daftar Komentar")

    if df_filtered is None:
        render_data_notice(
            "Dataset komentar belum ditemukan di folder data/processed/comments_clean.csv "
            "atau data/raw/comments_raw.csv. Tambahkan file dataset untuk melihat daftar komentar.",
            level="info",
        )
    elif df_filtered.empty:
        render_data_notice(
            "Tidak ada komentar yang sesuai dengan filter yang dipilih.",
            level="info",
        )
    else:
        if "ce_page" not in st.session_state:
            st.session_state["ce_page"] = 1

        page_size = 10
        df_page, total_pages = paginate(
            df_filtered, page=st.session_state["ce_page"], page_size=page_size
        )
        st.session_state["ce_page"] = max(1, min(st.session_state["ce_page"], total_pages))

        date_col = _get_col(df_page, "date", ("date", "tanggal", "created_at"))
        text_col = _get_col(df_page, "text", ("comment_text", "komentar", "text", "text_clean"))
        likes_col = _get_col(df_page, "likes", ("likes", "like_count", "like"))

        display_df = pd.DataFrame()
        display_df["Tanggal"] = (
            pd.to_datetime(df_page[date_col], errors="coerce").dt.strftime("%Y-%m-%d").fillna("-")
            if date_col
            else "-"
        )
        display_df["Topik"] = (
            df_page[topic_col].fillna(config.EMPTY_VALUE)
            if topic_col and topic_col in df_page.columns
            else config.EMPTY_VALUE
        )
        display_df["Komentar"] = df_page[text_col].fillna("") if text_col else ""
        display_df["Likes"] = (
            pd.to_numeric(df_page[likes_col], errors="coerce").fillna(0).astype(int)
            if likes_col
            else 0
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tanggal": st.column_config.TextColumn("Tanggal", width="small"),
                "Topik": st.column_config.TextColumn("Topik", width="medium"),
                "Komentar": st.column_config.TextColumn("Komentar", width="large"),
                "Likes": st.column_config.NumberColumn("Likes", width="small"),
            },
        )

        p_prev, p_info, p_next = st.columns([1.2, 2.6, 1.2])
        with p_prev:
            if st.button(
                "← Prev",
                key="ce_prev",
                disabled=st.session_state["ce_page"] <= 1,
                use_container_width=True,
            ):
                st.session_state["ce_page"] -= 1
                st.rerun()
        with p_info:
            st.markdown(
                f"<p style='text-align:center; margin-top:6px; font-size:0.9rem;'>"
                f"Hal. <b>{st.session_state['ce_page']}</b> / <b>{total_pages}</b> "
                f"({len(df_filtered):,} komentar)</p>",
                unsafe_allow_html=True,
            )
        with p_next:
            if st.button(
                "Next →",
                key="ce_next",
                disabled=st.session_state["ce_page"] >= total_pages,
                use_container_width=True,
            ):
                st.session_state["ce_page"] += 1
                st.rerun()


render()
