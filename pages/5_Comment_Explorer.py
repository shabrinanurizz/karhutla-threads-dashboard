"""Halaman Comment Explorer (Tahap 4)."""

import html
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

UNCLASSIFIED_LABEL = "Tidak Terklasifikasi"

# Pemetaan ID / nama generik topik ke label deskriptif sesuai halaman Modelling
DEFAULT_TOPIC_LABELS = {
    0: "Kritik ke Pemerintah dan Perusahaan",
    1: "Kondisi Kebakaran dan Lapangan",
    2: "Doa dan Kecaman Pembakaran",
    3: "Dampak Bencana dan Peran Sawit",
}

TOPIC_NAME_ALIASES = {
    "0": DEFAULT_TOPIC_LABELS[0],
    "topik 1": DEFAULT_TOPIC_LABELS[0],
    "topic 1": DEFAULT_TOPIC_LABELS[0],
    "topic_0": DEFAULT_TOPIC_LABELS[0],
    "1": DEFAULT_TOPIC_LABELS[1],
    "topik 2": DEFAULT_TOPIC_LABELS[1],
    "topic 2": DEFAULT_TOPIC_LABELS[1],
    "topic_1": DEFAULT_TOPIC_LABELS[1],
    "2": DEFAULT_TOPIC_LABELS[2],
    "topik 3": DEFAULT_TOPIC_LABELS[2],
    "topic 3": DEFAULT_TOPIC_LABELS[2],
    "topic_2": DEFAULT_TOPIC_LABELS[2],
    "3": DEFAULT_TOPIC_LABELS[3],
    "topik 4": DEFAULT_TOPIC_LABELS[3],
    "topic 4": DEFAULT_TOPIC_LABELS[3],
    "topic_3": DEFAULT_TOPIC_LABELS[3],
}

# Palet badge kapsul topik selaras dengan tema dashboard
TOPIC_BADGE_STYLES = {
    "Kritik ke Pemerintah dan Perusahaan": ("#E6F0EC", "#163E29", "#B7D1C6"),
    "Kondisi Kebakaran dan Lapangan": ("#FDECE6", "#C84617", "#F6C3B0"),
    "Doa dan Kecaman Pembakaran": ("#F9F2E4", "#9A6E24", "#E8D4AE"),
    "Dampak Bencana dan Peran Sawit": ("#FEF5E4", "#B87314", "#F7DBA3"),
    UNCLASSIFIED_LABEL: ("#F1F3F2", "#5C6661", "#D5DBD8"),
}

SORT_BUTTON_LABELS = {
    "Default": "⇅ Urutkan",
    "Likes Asc": "↑ Likes",
    "Likes Desc": "↓ Likes",
    "Tanggal Asc": "↑ Tanggal",
    "Tanggal Desc": "↓ Tanggal",
}


def _set_sort_option(option: str):
    """Simpan opsi urutan global dan kembalikan pagination ke halaman 1."""
    st.session_state["ce_sort"] = option
    st.session_state["ce_page"] = 1


def _sort_comments(df: pd.DataFrame | None, sort_option: str) -> pd.DataFrame | None:
    """Urutkan seluruh komentar secara global sebelum dipotong per halaman."""
    if df is None or df.empty or sort_option == "Default":
        return df

    df_sorted = df.copy()
    ascending = sort_option.endswith("Asc")

    if sort_option.startswith("Likes"):
        likes_col = _get_col(df_sorted, "likes", ("likes", "like_count", "like"))
        if likes_col:
            df_sorted["_sort_key"] = pd.to_numeric(
                df_sorted[likes_col], errors="coerce"
            ).fillna(0)
            df_sorted = df_sorted.sort_values(
                by="_sort_key",
                ascending=ascending,
                na_position="last",
                kind="mergesort",
            ).drop(columns=["_sort_key"])
    elif sort_option.startswith("Tanggal"):
        date_col = _get_col(df_sorted, "date", ("date", "tanggal", "created_at"))
        if date_col:
            df_sorted["_sort_key"] = pd.to_datetime(
                df_sorted[date_col], errors="coerce"
            )
            df_sorted = df_sorted.sort_values(
                by="_sort_key",
                ascending=ascending,
                na_position="last",
                kind="mergesort",
            ).drop(columns=["_sort_key"])

    return df_sorted


def _get_topic_label_map() -> dict[int, str]:
    """Ambil kamus label topik dari src.topic_modeling jika tersedia, atau gunakan default."""
    label_map = dict(DEFAULT_TOPIC_LABELS)
    try:
        from src import topic_modeling

        for attr in ("TOPIC_LABELS", "TOPIC_NAMES", "LABELS"):
            custom = getattr(topic_modeling, attr, None)
            if isinstance(custom, dict) and custom:
                for k, v in custom.items():
                    try:
                        label_map[int(k)] = str(v)
                    except (ValueError, TypeError):
                        pass
                break
            if isinstance(custom, (list, tuple)) and custom:
                for idx, v in enumerate(custom):
                    label_map[idx] = str(v)
                break
    except Exception:
        pass
    return label_map


def _render_summary_card(label: str, value: str):
    """Render kartu ringkasan horizontal yang proporsional untuk tampilan satu layar penuh."""
    st.markdown(
        f"""
        <div style="
            background-color: {config.COLORS['green_dark']};
            color: {config.COLORS['text_light']};
            padding: 12px 18px;
            border-radius: {config.LAYOUT['card_radius']};
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            font-family: '{config.FONT_FAMILY}', sans-serif;
            min-height: 76px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9; margin-bottom: 3px;">
                {label}
            </div>
            <div style="font-size: 1.2rem; font-weight: 800; line-height: 1.2;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_topic_pill(topic_name: str) -> str:
    """Bangun HTML badge kapsul berwarna untuk kolom Topik."""
    clean_topic = str(topic_name).strip()
    if clean_topic == "" or clean_topic == config.EMPTY_VALUE:
        clean_topic = UNCLASSIFIED_LABEL
    escaped = html.escape(clean_topic)

    bg, fg, border = TOPIC_BADGE_STYLES.get(
        clean_topic, ("#EBF1EE", "#1E4632", "#C4D6CC")
    )
    extra_style = "font-style:italic;" if clean_topic == UNCLASSIFIED_LABEL else ""
    return (
        f'<span style="display:inline-block; padding:4px 11px; border-radius:999px; '
        f'background-color:{bg}; color:{fg}; border:1px solid {border}; '
        f'font-size:0.76rem; font-weight:600; line-height:1.25; {extra_style}">'
        f"{escaped}</span>"
    )


def _inject_fullscreen_layout_css():
    """Atur padding layar penuh dan tombol popover urutan agar pas satu viewport."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.35rem !important;
            padding-bottom: 0.75rem !important;
            padding-left: 2.2rem !important;
            padding-right: 2.2rem !important;
            max-width: 100% !important;
        }
        [data-testid="stPopover"] {
            margin-top: 14px !important;
        }
        [data-testid="stPopover"] > button {
            border-radius: 10px !important;
            border: 1px solid rgba(22, 62, 41, 0.22) !important;
            background-color: #FFFFFF !important;
            color: #163E29 !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            padding: 0.32rem 0.75rem !important;
            min-height: 36px !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
        }
        [data-testid="stPopover"] > button:hover {
            background-color: #F1F6F3 !important;
            border-color: #163E29 !important;
        }
        [data-testid="stPopoverBody"] {
            min-width: 210px !important;
            max-width: 230px !important;
            padding: 8px !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
        }
        [data-testid="stPopoverBody"] button {
            justify-content: flex-start !important;
            text-align: left !important;
            border: none !important;
            background: transparent !important;
            color: #2C3531 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            padding: 0.36rem 0.65rem !important;
            min-height: 32px !important;
            border-radius: 8px !important;
        }
        [data-testid="stPopoverBody"] button:hover {
            background-color: #F3F5F2 !important;
            color: #163E29 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_modern_comments_table(display_df: pd.DataFrame, sort_option: str = "Default"):
    """Render tabel Daftar Komentar modern yang mengisi penuh layar secara proporsional."""
    green_dark = config.COLORS.get("green_dark", "#163E29")
    text_light = config.COLORS.get("text_light", "#F5F3EB")
    font_family = config.FONT_FAMILY

    arrow = "↑" if sort_option.endswith("Asc") else "↓"
    tgl_header = f"Tanggal {arrow}" if sort_option.startswith("Tanggal") else "Tanggal"
    likes_header = f"Likes {arrow}" if sort_option.startswith("Likes") else "Likes"

    css = f"""
<style>
.ce-table-wrapper {{
    width: 100%;
    border-radius: 14px;
    overflow: hidden;
    background-color: #FFFFFF;
    border: 1px solid rgba(22, 62, 41, 0.14);
    box-shadow: 0 4px 16px rgba(22, 62, 41, 0.07);
    margin-bottom: 10px;
    font-family: '{font_family}', sans-serif;
}}
.ce-modern-table {{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.88rem;
}}
.ce-modern-table thead tr {{
    background-color: {green_dark};
    color: {text_light};
}}
.ce-modern-table th {{
    padding: 11px 16px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border: none;
}}
.ce-modern-table td {{
    padding: 10px 16px;
    border-bottom: 1px solid #EEF1EF;
    vertical-align: middle;
    color: #1F2924;
    height: 52px;
}}
.ce-modern-table tbody tr:last-child td {{
    border-bottom: none;
}}
.ce-modern-table tbody tr:nth-child(even) {{
    background-color: #FAFBF9;
}}
.ce-modern-table tbody tr:hover {{
    background-color: #F1F6F3;
    transition: background-color 0.15s ease;
}}
.ce-col-date {{
    white-space: nowrap;
    color: #55625C !important;
    font-size: 0.83rem;
    font-weight: 500;
    width: 115px;
}}
.ce-col-topic {{
    width: 265px;
}}
.ce-col-comment {{
    line-height: 1.38;
}}
.ce-comment-clamp {{
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    word-break: break-word;
}}
.ce-col-likes {{
    text-align: right;
    white-space: nowrap;
    width: 105px;
}}
.ce-likes-pill {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background-color: #F4F6F5;
    color: #2C3A33;
    font-weight: 700;
    font-size: 0.8rem;
}}
.ce-likes-pill.has-likes {{
    background-color: #FDECE6;
    color: #C84617;
}}
</style>
"""

    rows_html = []
    for _, row in display_df.iterrows():
        tgl = html.escape(str(row["Tanggal"]))
        topik_badge = _render_topic_pill(str(row["Topik"]))
        komentar = html.escape(str(row["Komentar"]))
        likes_num = int(row["Likes"])
        likes_cls = "ce-likes-pill has-likes" if likes_num > 0 else "ce-likes-pill"

        rows_html.append(
            "<tr>"
            f'<td class="ce-col-date">{tgl}</td>'
            f'<td class="ce-col-topic">{topik_badge}</td>'
            f'<td class="ce-col-comment" title="{komentar}"><div class="ce-comment-clamp">{komentar}</div></td>'
            f'<td class="ce-col-likes"><span class="{likes_cls}">♥ {likes_num:,}</span></td>'
            "</tr>"
        )

    table_html = (
        css
        + '<div class="ce-table-wrapper">'
        + '<table class="ce-modern-table">'
        + "<thead><tr>"
        + f"<th>{tgl_header}</th>"
        + "<th>Topik</th>"
        + "<th>Komentar</th>"
        + f'<th style="text-align:right;">{likes_header}</th>'
        + "</tr></thead>"
        + "<tbody>"
        + "".join(rows_html)
        + "</tbody></table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def _format_topic_series(series: pd.Series) -> pd.Series:
    """Ubah ID angka atau 'Topik 1..4' menjadi nama kategori topik sesuai halaman Modelling."""
    label_map = _get_topic_label_map()
    aliases = dict(TOPIC_NAME_ALIASES)
    for idx, name in label_map.items():
        aliases[str(idx)] = name
        aliases[f"topik {idx + 1}"] = name
        aliases[f"topic {idx + 1}"] = name
        aliases[f"topic_{idx}"] = name

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
                return label_map.get(num, f"Topik {num + 1}" if num >= 0 else s)
        except ValueError:
            pass
        return aliases.get(s.lower(), s)

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
        std_topic_col = config.COLUMNS.get("topic", "topic")
        df[std_topic_col] = formatted
        df["topic"] = formatted

    return df


def render():
    render_page_title("COMMENT EXPLORER")
    _inject_fullscreen_layout_css()

    if "ce_sort" not in st.session_state:
        st.session_state["ce_sort"] = "Default"

    df = _load_explorer_data()

    label_map = _get_topic_label_map()
    topic_options = list(label_map.values())
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

    if UNCLASSIFIED_LABEL not in topic_options:
        topic_options = [*topic_options, UNCLASSIFIED_LABEL]

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

    # Terapkan filter tanggal & kata kunci, lalu filter topik
    df_filtered = filter_comments(
        df,
        date_range=(date_from, date_to),
        topic=None,
        query=search_query,
    )
    if (
        df_filtered is not None
        and selected_topic
        and topic_col
        and topic_col in df_filtered.columns
    ):
        if selected_topic == UNCLASSIFIED_LABEL:
            df_filtered = df_filtered[
                df_filtered[topic_col].isna()
                | (
                    df_filtered[topic_col]
                    .astype(str)
                    .str.strip()
                    .isin(["", config.EMPTY_VALUE, UNCLASSIFIED_LABEL])
                )
            ]
        else:
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
        else (
            UNCLASSIFIED_LABEL
            if selected_topic == UNCLASSIFIED_LABEL
            else config.EMPTY_VALUE
        )
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

    # ------------------------------------------------------------------
    # Baris 3: Header Daftar Komentar + Tombol Popover Urutan Ringkas
    # ------------------------------------------------------------------
    hdr_col, sort_btn_col = st.columns([4.6, 1.1])
    with hdr_col:
        render_section_header("Daftar Komentar")
    with sort_btn_col:
        current_sort = st.session_state["ce_sort"]
        btn_label = SORT_BUTTON_LABELS.get(current_sort, "⇅ Urutkan")
        with st.popover(btn_label, use_container_width=True):
            st.markdown(
                "<div style='font-size:0.75rem; font-weight:700; color:#5C6661; "
                "padding:2px 8px 6px 8px; border-bottom:1px solid #ECEFED; margin-bottom:4px;'>"
                "Urutkan Semua Data</div>",
                unsafe_allow_html=True,
            )
            menu_items = [
                ("↑  Likes ascending", "Likes Asc"),
                ("↓  Likes descending", "Likes Desc"),
                ("↑  Tanggal ascending", "Tanggal Asc"),
                ("↓  Tanggal descending", "Tanggal Desc"),
                ("↺  Default", "Default"),
            ]
            for label, opt_val in menu_items:
                prefix = "✓ " if current_sort == opt_val else ""
                if st.button(
                    f"{prefix}{label}",
                    key=f"ce_opt_{opt_val}",
                    use_container_width=True,
                ):
                    _set_sort_option(opt_val)
                    st.rerun()

    # Urutkan SELURUH komentar sebelum dipotong per halaman
    df_sorted = _sort_comments(df_filtered, st.session_state["ce_sort"])

    if df_sorted is None:
        render_data_notice(
            "Dataset komentar belum ditemukan di folder data/processed/comments_clean.csv "
            "atau data/raw/comments_raw.csv. Tambahkan file dataset untuk melihat daftar komentar.",
            level="info",
        )
    elif df_sorted.empty:
        render_data_notice(
            "Tidak ada komentar yang sesuai dengan filter yang dipilih.",
            level="info",
        )
    else:
        if "ce_page" not in st.session_state:
            st.session_state["ce_page"] = 1

        page_size = 5
        df_page, total_pages = paginate(
            df_sorted, page=st.session_state["ce_page"], page_size=page_size
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
            df_page[topic_col]
            .replace(["", config.EMPTY_VALUE], pd.NA)
            .fillna(UNCLASSIFIED_LABEL)
            if topic_col and topic_col in df_page.columns
            else UNCLASSIFIED_LABEL
        )
        display_df["Komentar"] = df_page[text_col].fillna("") if text_col else ""
        display_df["Likes"] = (
            pd.to_numeric(df_page[likes_col], errors="coerce").fillna(0).astype(int)
            if likes_col
            else 0
        )

        _render_modern_comments_table(display_df, sort_option=st.session_state["ce_sort"])

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
                f"<p style='text-align:center; margin-top:6px; font-size:0.88rem;'>"
                f"Hal. <b>{st.session_state['ce_page']}</b> / <b>{total_pages}</b> "
                f"({len(df_sorted):,} komentar)</p>",
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