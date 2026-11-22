"""Halaman Co-occurrence Analysis.

Layout mengikuti desain:
  1. Panel hijau atas : kartu krem berisi filter "Minimal kata muncul bersama" + jaringan kata
  2. Panel hijau bawah: dua kartu krem berdampingan
        - kiri : Top 10 Pasangan Kata (bar chart horizontal)
        - kanan: Network Kata Target (input kata target di header kartu)

Logika perhitungan ada di `src/cooccurrence.py`, komponen chart di `src/visualization.py`.
Gaya khusus halaman ini (CSS di bawah) hanya aktif di halaman ini, `assets/style.css` tidak diubah.
"""

import streamlit as st

from src import config
import src.cooccurrence as cooc
import src.visualization as viz
from src.cooccurrence import (
    tokenize_texts,
    calculate_cooccurrence,
    get_top_pairs,
    get_most_connected_word,
    build_network_graph,
    build_target_graph,
)
from src.data_loader import load_processed_data
from src.visualization import (
    render_page_title,
    render_placeholder_card,
    render_data_notice,
    render_ranked_bar_chart,
    render_network_graph,
)

# ---------------------------------------------------------------------------
# Pengaturan (ubah di sini untuk menyesuaikan tampilan)
# ---------------------------------------------------------------------------
DEFAULT_MIN_COOCCUR = 40   # ~60 kata pada dataset saat ini
MAX_EDGES = 250            # batas garis supaya grafik tetap terbaca
BASE_MIN_COOCCUR = 2       # ambang dasar perhitungan (filter di atasnya dilakukan di memori)

SCALE = 1.4                              # satu angka untuk membesar/mengecilkan semua plot
MAIN_CHART_H = int(230 * SCALE)          # tinggi plot jaringan utama (px)
BOTTOM_CHART_H = int(215 * SCALE)        # tinggi plot Network Kata Target (px)
TOP10_CHART_H = BOTTOM_CHART_H + 30      # bar chart sedikit lebih tinggi karena headernya lebih pendek
BOTTOM_CARD_H = BOTTOM_CHART_H + 80      # tinggi minimum dua kartu bawah (dibuat sama)

PAGE_CSS = """
<style>
/* ---- Kompak: kurangi ruang kosong ---- */
[data-testid="stMainBlockContainer"] { padding-top: 1.2rem !important; padding-bottom: 0.6rem !important; }
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] { gap: 0.55rem; }
[data-testid="stForm"] { padding: 0 !important; }

/* ---- Judul kartu (sub-judul tiap plot) ---- */
.co-title { color: #1B4332; font-weight: 800; font-size: 1.3rem; line-height: 1.15; margin: 0; padding-bottom: 14px; }
.co-info { color: #1B4332; opacity: 0.7; font-weight: 600; font-size: 0.85rem; text-align: right; }

/* ---- Input: satu pil bersih (tanpa kotak putih di belakangnya) ---- */
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="input"] {
  background: #FDF9EE !important; border: 1px solid rgba(27, 67, 50, 0.18) !important;
  border-radius: 999px !important; box-shadow: 0 4px 10px rgba(27, 67, 50, 0.15) !important;
  overflow: hidden;
}
div[data-testid="stNumberInput"] div[data-baseweb="base-input"],
div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
  background: transparent !important; border: none !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
  background: transparent !important; box-shadow: none !important; border-radius: 0 !important;
}
div[data-testid="stNumberInput"] button {
  background: transparent !important; box-shadow: none !important; color: #1B4332 !important;
}
div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
  outline: 2px solid #E85D10; outline-offset: 0;
}

/* ---- Tombol apply: teks penuh terbaca, padding kecil ---- */
.stFormSubmitButton > button, .stButton > button {
  padding: 0.45rem 0.6rem !important; min-height: 0 !important; white-space: nowrap !important;
}
.stFormSubmitButton > button *, .stButton > button * {
  white-space: nowrap !important; overflow: visible !important; text-overflow: clip !important;
}

/* ---- Panel hijau + kartu krem di dalamnya (seperti banner Latar Belakang / Tujuan) ---- */
.st-key-co_panel_main, .st-key-co_panel_bottom {
  background: #1B4332 !important; border-radius: 8px !important; padding: 12px !important;
  box-shadow: 0 6px 14px rgba(27, 67, 50, 0.18) !important; gap: 0 !important;
}
.st-key-co_panel_bottom [data-testid="stHorizontalBlock"] { gap: 12px !important; }
.st-key-co_inner_main, .st-key-co_inner_top, .st-key-co_inner_target {
  background: #FDF9EE !important; border-radius: 8px !important;
  padding: 8px 14px 6px 14px !important; gap: 0.25rem !important;
}
/* dua kartu bawah selalu sama tinggi */
.st-key-co_inner_top, .st-key-co_inner_target { min-height: __CARD_H__px; }
</style>
""".replace("__CARD_H__", str(BOTTOM_CARD_H))


def _card_title(text: str):
    st.markdown(f"<div class='co-title'>{text}</div>", unsafe_allow_html=True)


@st.cache_data(show_spinner="Menghitung co-occurrence...")
def _compute_base_cooccurrence(texts: tuple, stopword_count: int):
    """Hitung semua pasangan kata (>= 2x) sekali saja; hasil di-cache.

    `stopword_count` hanya untuk menyegarkan cache saat daftar stopword berubah.
    """
    return calculate_cooccurrence(tokenize_texts(list(texts)), min_cooccur=BASE_MIN_COOCCUR)


def _files_are_current() -> bool:
    """Pastikan src/cooccurrence.py dan src/visualization.py sudah versi terbaru."""
    ok = True
    if not hasattr(viz, "_packed_layout"):
        st.error("`src/visualization.py` di project kamu masih versi lama. "
                 "Timpa dengan versi terbaru, lalu refresh halaman (Ctrl + F5).")
        ok = False
    if getattr(cooc, "STOPWORDS_VERSION", 0) < 3:
        st.error("`src/cooccurrence.py` di project kamu masih versi lama (stopword belum lengkap). "
                 "Timpa dengan versi terbaru, lalu refresh halaman (Ctrl + F5).")
        ok = False
    return ok


def render():
    st.markdown(PAGE_CSS, unsafe_allow_html=True)
    render_page_title("CO- OCCURRENCE ANALYSIS")

    if not _files_are_current():
        st.stop()

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
        render_data_notice(f"Kolom teks '{text_col}' tidak ditemukan dalam dataset.", level="warning")
        return

    texts = tuple(df[text_col].dropna().astype(str).tolist())
    co_all = _compute_base_cooccurrence(texts, len(cooc._STOPWORDS_ID))
    if co_all is None:
        render_data_notice("Tidak ada pasangan kata yang dapat dihitung dari dataset.", level="warning")
        return

    # ------------------------------------------------------------------
    # Panel atas: filter (header kartu) + jaringan kata
    # ------------------------------------------------------------------
    with st.container(key="co_panel_main"):
        with st.container(key="co_inner_main"):
            # Form -> nilai filter hanya berubah saat 'apply' diklik
            with st.form("co_filter_form", border=False):
                c_title, c_input, c_btn, c_info = st.columns(
                    [3.2, 1.6, 0.9, 2.6], vertical_alignment="center"
                )
                with c_title:
                    _card_title("Minimal kata muncul bersama")
                with c_input:
                    st.number_input(
                        "Minimal kata muncul bersama",
                        min_value=BASE_MIN_COOCCUR, value=DEFAULT_MIN_COOCCUR, step=1,
                        key="co_min", label_visibility="collapsed",
                    )
                with c_btn:
                    st.form_submit_button("apply", use_container_width=True)
                with c_info:
                    info_slot = st.empty()

            min_cooccur = st.session_state.get("co_min", DEFAULT_MIN_COOCCUR)
            co_df = co_all[co_all["jumlah"] >= min_cooccur].reset_index(drop=True)

            if len(co_df) == 0:
                info_slot.markdown("<div class='co-info'>tidak ada pasangan</div>", unsafe_allow_html=True)
                render_placeholder_card(
                    "Jaringan Kata (Co-occurrence Network)",
                    f"Tidak ada pasangan kata yang muncul bersama minimal {min_cooccur}x. "
                    "Coba turunkan nilai filter.",
                )
            else:
                graph = build_network_graph(co_df, max_edges=MAX_EDGES)
                info_slot.markdown(
                    f"<div class='co-info'>{graph.number_of_nodes()} kata · "
                    f"{graph.number_of_edges()} pasangan</div>",
                    unsafe_allow_html=True,
                )
                render_network_graph(graph, height=MAIN_CHART_H, key="main")

    # ------------------------------------------------------------------
    # Panel bawah: satu panel hijau, dua kartu krem
    # ------------------------------------------------------------------
    default_word = get_most_connected_word(co_df) if len(co_df) else None

    with st.container(key="co_panel_bottom"):
        col_a, col_b = st.columns(2)

        # ---- Kiri: Top 10 Pasangan Kata
        with col_a:
            with st.container(key="co_inner_top"):
                _card_title("Top 10 Pasangan Kata")
                top_pairs = get_top_pairs(co_df, top_n=10)
                if top_pairs is None:
                    render_placeholder_card(
                        "Top 10 Pasangan Kata", "Tidak ada pasangan kata yang memenuhi filter."
                    )
                else:
                    top_pairs["pasangan"] = top_pairs["kata_a"] + " – " + top_pairs["kata_b"]
                    render_ranked_bar_chart(
                        top_pairs, "pasangan", "jumlah", height=TOP10_CHART_H, key="top_pairs", font_size=13
                    )

        # ---- Kanan: Network Kata Target
        with col_b:
            with st.container(key="co_inner_target"):
                c_title, c_input, c_btn = st.columns([2.4, 2.8, 1.2], vertical_alignment="center")
                with c_title:
                    _card_title("Network Kata Target")
                with c_input:
                    st.text_input(
                        "Kata target",
                        placeholder=f"default: {default_word}" if default_word else "ketik kata",
                        key="co_target",
                        label_visibility="collapsed",
                    )
                with c_btn:
                    st.button("apply", key="co_target_apply", use_container_width=True)

                kata_target = st.session_state.get("co_target", "").strip().lower()
                target = kata_target or default_word

                if not target:
                    render_placeholder_card("Network Kata Target", "Belum ada data untuk ditampilkan.")
                else:
                    # Kata target memakai seluruh pasangan (>= 2x) supaya tetap punya tetangga
                    # walaupun filter utama tinggi.
                    t_graph = build_target_graph(co_all, target, max_neighbors=15)
                    if t_graph is None:
                        render_placeholder_card(
                            "Network Kata Target",
                            f"Kata '{target}' tidak ditemukan atau tidak punya pasangan kata. "
                            "Coba bentuk kata dasar, mis. 'bakar'.",
                        )
                    else:
                        render_network_graph(
                            t_graph, height=BOTTOM_CHART_H, key="target", center=target
                        )


render()
