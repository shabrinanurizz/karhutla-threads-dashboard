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
    "topic",
    "topik",
    "dominant_topic",
    "topic_label",
    "topic_id",
    "lda_topic",
    "cluster",
)


def _render_summary_card(label: str, value: str):
    """Render kartu ringkasan dengan latar hijau tua agar kontras dengan teks putih."""
    st.markdown(
        f"""
        <div style="
            background-color: {config.COLORS['green_dark']};
            color: {config.COLORS['text_light']};
            padding: 18px 20px;
            border-radius: {config.LAYOUT['card_radius']};
            margin-bottom: 14px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            font-family: '{config.FONT_FAMILY}', sans-serif;
        ">
            <div style="font-size: 0.9rem; font-weight: 600; opacity: 0.9; margin-bottom: 6px;">
                {label}
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; letter-spacing: 0.5px;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _format_topic_series(series: pd.Series) -> pd.Series:
    """Rapikan label topik (misal angka 0/1/2 menjadi 'Topik 1', 'Topik 2', dst.)."""
    def _clean_val(val):
        if pd.isna(val) or str(val).strip() == "":
            return config.EMPTY_VALUE
        s = str(val).strip()
        if s.isdigit():
            num = int(s)
            return f"Topik {num + 1}" if num == 0 else f"Topik {num}"
        return s

    return series.apply(_clean_val)


def _load_explorer_data() -> pd.DataFrame | None:
    """Memuat dataset komentar dan menggabungkan hasil topik jika tersedia."""
    df = load_processed_data()
    if df is None:
        df = load_raw_data()
    if df is None:
        return None

    df = df.copy()
    topic_col = _get_col(df, "topic", TOPIC_COL_CANDIDATES)

    # Jika kolom topik belum ada di comments_clean.csv, cek folder data/model_output
    if topic_col is None:
        df_model = load_dataset(config.MODEL_OUTPUT_DIR)
        if df_model is not None:
            model_topic_col = _get_col(df_model, "topic", TOPIC_COL_CANDIDATES)
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

    topic_col = _get_col(df, "topic", TOPIC_COL_CANDIDATES)
    if topic_col is not None:
        df[topic_col] = _format_topic_series(df[topic_col])

    return df


def render():
    render_page_title("COMMENT EXPLORER")

    df = _load_explorer_data()

    # Ambil daftar topik unik dari dataset jika tersedia
    topic_options = ["Topik 1", "Topik 2", "Topik 3", "Topik 4"]
    topic_col = None
    if df is not None:
        topic_col = _get_col(df, "topic", TOPIC_COL_CANDIDATES)
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
    # Baris filter: Dari tanggal, Sampai tanggal, Topik, Cari Komentar, apply
    # ------------------------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns([1.6, 1.6, 1.6, 2.2, 0.9])
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

    if df is not None and topic_col is None:
        st.caption(
            "ℹ️ Data topik belum tersedia di `data/model_output/` (menunggu hasil bagian Topic Modelling), "
            "sehingga kolom dan filter topik masih menampilkan `—`."
        )

    st.divider()

    # Terapkan filter & hitung ringkasan
    df_filtered = filter_comments(
        df,
        date_range=(date_from, date_to),
        topic=selected_topic,
        query=search_query,
    )
    stats = summary_stats(df_filtered)

    # ------------------------------------------------------------------
    # Panel kiri: Ringkasan
    # Panel kanan: Daftar Komentar (tabel dengan pagination)
    # ------------------------------------------------------------------
    col_left, col_right = st.columns([0.32, 0.68])

    with col_left:
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

        _render_summary_card("Total komentar", total_val)
        _render_summary_card("Topik terbanyak", top_topic_val)
        _render_summary_card("Rata-rata likes", avg_likes_val)

    with col_right:
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

            # Susun kolom tampilan tabel: Tanggal | Topik | Komentar | Likes
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

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Kontrol Pagination
            p_prev, p_info, p_next = st.columns([1.2, 2.6, 1.2])
            with p_prev:
                if st.button(
                    "← Sebelumnya",
                    key="ce_prev",
                    disabled=st.session_state["ce_page"] <= 1,
                    use_container_width=True,
                ):
                    st.session_state["ce_page"] -= 1
                    st.rerun()
            with p_info:
                st.markdown(
                    f"<p style='text-align:center; margin-top:6px;'>"
                    f"Halaman <b>{st.session_state['ce_page']}</b> dari <b>{total_pages}</b> "
                    f"({len(df_filtered):,} komentar)</p>",
                    unsafe_allow_html=True,
                )
            with p_next:
                if st.button(
                    "Berikutnya →",
                    key="ce_next",
                    disabled=st.session_state["ce_page"] >= total_pages,
                    use_container_width=True,
                ):
                    st.session_state["ce_page"] += 1
                    st.rerun()


render()
