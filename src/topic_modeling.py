"""Halaman 4 - Topic Analysis (Anggota 5).

Modul ini TIDAK melatih model. Model dilatih di notebooks/04_topic_modeling.ipynb,
hasilnya disimpan ke data/model_output/*.csv, lalu dibaca di sini.

Fungsi utama (sesuai Function Contract):
    show_topic_analysis(data, topics, words, metrics, comparison=None)

Parameter:
    data        : DataFrame komentar (kolom wajib: comment_id, date, likes, replies;
                  kolom shares opsional)
    topics      : DataFrame topic_assignments (comment_id, topic_id, topic_name)
    words       : DataFrame topic_words (topic_id, word, weight, rank)
    metrics     : DataFrame topic_metrics (model_name, n_topics, coherence_score, ...)
    comparison  : DataFrame topic_comparison (topic_id, lambda, word, weight, rank),
                  opsional. Jika None, slider lambda disembunyikan.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src import config
from src.visualization import render_page_title

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "model_output"
TOP_N = 8

# Warna topik dari palet global (urutan: hijau tua, oranye-merah, amber, emas, ...)
PALET = config.CHART_COLORWAY

# Warna grup KPI — 4 warna berbeda dari config.COLORS
_KPI = {
    "komentar": config.COLORS["green_dark"],   # #1B4332
    "likes":    config.COLORS["red_orange"],   # #D94A05
    "replies":  config.COLORS["amber"],        # #F58E0A
    "shares":   config.COLORS["orange"],       # #E85D10
}


# ---------- LOADER (sementara; pindah ke data_loader.py jika Anggota 2 menyediakan) ----------
def _baca(nama_file):
    path = DATA_DIR / nama_file
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    return pd.read_csv(path)


def load_topic_assignments():
    return _baca("topic_assignments.csv")


def load_topic_words():
    return _baca("topic_words.csv")


def load_topic_metrics():
    return _baca("topic_metrics.csv")


def load_topic_comparison():
    return _baca("topic_comparison.csv")


# ---------- PERHITUNGAN (tanpa Streamlit, mudah dites) ----------
def gabung_data(data, topics):
    """Gabungkan komentar dengan label topiknya (kunci: comment_id)."""
    wajib = {"comment_id", "date", "likes", "replies"}
    kurang = wajib - set(data.columns)
    if kurang:
        raise ValueError(f"Kolom data tidak lengkap: {sorted(kurang)}")
    gabung = topics.merge(data, on="comment_id", how="inner")
    gabung["date"] = pd.to_datetime(gabung["date"], errors="coerce")
    return gabung


def ambil_top_kata(words, comparison, topic_id, lam, n=TOP_N):
    """Top-n kata satu topik. Pakai topic_comparison (per lambda) jika ada,
    selain itu pakai topic_words (urut rank)."""
    if comparison is not None:
        c = comparison[(comparison["topic_id"] == topic_id)
                       & np.isclose(comparison["lambda"], lam)]
        c = c.sort_values("rank").head(n).copy()
        c["skor"] = np.exp(c["weight"] - c["weight"].max())
        return c[["word", "skor"]]
    w = words[words["topic_id"] == topic_id].sort_values("rank").head(n).copy()
    w["skor"] = w["weight"] / w["weight"].max()
    return w[["word", "skor"]]


def ringkasan_topik(gabung, nama_topik):
    d = gabung[gabung["topic_name"] == nama_topik]
    return {
        "komentar": len(d),
        "likes":   round(d["likes"].mean(), 1) if len(d) else 0,
        "replies": round(d["replies"].mean(), 1) if len(d) else 0,
        "shares":  round(d["shares"].mean(), 1) if ("shares" in d.columns and len(d)) else None,
    }


# ---------- HELPER RENDER ----------
def _tema_fig(fig, height, margin=None):
    """Terapkan tema global (latar transparan, teks gelap) ke figure Plotly."""
    fig.update_layout(
        paper_bgcolor=config.CHART["paper_bgcolor"],
        plot_bgcolor=config.CHART["plot_bgcolor"],
        font={"family": config.CHART["font_family"],
              "color": config.CHART["font_color"]},
        height=height,
        margin=margin or dict(l=5, r=5, t=36, b=5),
    )
    return fig


def _kpi_grup(col, label, warna, nama_a, val_a, nama_b, val_b):
    """Render satu grup KPI (header + 2 value box) ke dalam kolom Streamlit."""
    col.markdown(f"""
<div style="background:{warna};border-radius:9px;padding:6px 6px;
            text-align:center;color:white;">
  <div style="font-size:0.74rem;font-weight:700;margin-bottom:5px;
              letter-spacing:0.02em;">{label}</div>
  <div style="display:flex;gap:5px;">
    <div style="background:rgba(0,0,0,0.28);border-radius:6px;flex:1;padding:5px 3px;">
      <div style="font-size:0.63rem;font-weight:600;margin-bottom:2px;
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{nama_a}</div>
      <div style="font-size:1.1rem;font-weight:700;line-height:1.1;">{val_a}</div>
    </div>
    <div style="background:rgba(0,0,0,0.28);border-radius:6px;flex:1;padding:5px 3px;">
      <div style="font-size:0.63rem;font-weight:600;margin-bottom:2px;
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{nama_b}</div>
      <div style="font-size:1.1rem;font-weight:700;line-height:1.1;">{val_b}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)


def _bar_kata(words, comparison, topic_id, lam, nama, warna_bar):
    """Bar chart horizontal top kata satu topik."""
    top = ambil_top_kata(words, comparison, topic_id, lam).sort_values("skor")
    fig = px.bar(top, x="skor", y="word", orientation="h",
                 title=f"Top {TOP_N} Kata — {nama}",
                 labels={"skor": "", "word": ""})
    fig.update_traces(marker_color=warna_bar)
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(tickfont=dict(size=11,
                                 color=config.CHART["font_color"])),
        title_font=dict(size=12, color=config.CHART["font_color"]),
    )
    return _tema_fig(fig, height=220)


# ---------- TAMPILAN UTAMA ----------
def show_topic_analysis(data, topics, words, metrics, comparison=None):
    if data is None or len(data) == 0 or topics is None or len(topics) == 0:
        st.warning("Data komentar atau hasil topik kosong.")
        return
    gabung = gabung_data(data, topics)
    if gabung.empty:
        st.warning("Tidak ada comment_id yang cocok antara data komentar dan hasil topik.")
        return

    daftar = (topics.drop_duplicates("topic_id").sort_values("topic_id")
              [["topic_id", "topic_name"]])
    nama_ke_id = dict(zip(daftar["topic_name"], daftar["topic_id"]))
    topik = list(nama_ke_id)
    warna = dict(zip(topik, PALET))

    # CSS lokal — hanya untuk kompaksi jarak; warna/font sudah diatur style.css global
    st.markdown("""
<style>
.block-container {padding-top: 0.5rem !important; padding-bottom: 0.2rem !important;}
.stDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {gap: 0.25rem !important;}
.element-container {margin-bottom: 0.1rem !important;}
</style>""", unsafe_allow_html=True)

    render_page_title("PERBANDINGAN TOPIK")

    # ── BARIS 1: Donut (kiri) + Coherence (kanan) ───────────────────────────
    col_donut, col_coh = st.columns(2)

    with col_donut:
        with st.container(border=True):
            prop = gabung["topic_name"].value_counts().reset_index()
            prop.columns = ["topik", "jumlah"]
            fig = px.pie(prop, names="topik", values="jumlah", hole=0.42,
                         color="topik", color_discrete_map=warna,
                         title="Proporsi Komentar per Topik")
            fig.update_layout(legend_title_text="",
                              title_font=dict(color=config.CHART["font_color"]))
            st.plotly_chart(_tema_fig(fig, height=220), use_container_width=True)

    with col_coh:
        with st.container(border=True):
            k_dipakai = len(topik)
            fig = px.line(metrics, x="n_topics", y="coherence_score", markers=True,
                          title="Skor Koherens",
                          labels={"n_topics": "Jumlah Topik",
                                  "coherence_score": "Koherens"})
            fig.update_traces(line_color=config.COLORS["green_dark"],
                              marker_color=config.COLORS["green_dark"])
            baris_k = metrics[metrics["n_topics"] == k_dipakai]
            if not baris_k.empty:
                fig.add_annotation(
                    x=k_dipakai,
                    y=baris_k["coherence_score"].iloc[0],
                    text=f"Dipakai: K={k_dipakai}",
                    showarrow=True, arrowhead=2,
                    arrowcolor=config.COLORS["red_orange"],
                    font=dict(color=config.COLORS["red_orange"], size=11),
                    bgcolor=config.COLORS["cream_light"],
                    bordercolor=config.COLORS["red_orange"], borderpad=3,
                )
            fig.update_layout(
                xaxis=dict(gridcolor="rgba(27,67,50,0.1)"),
                yaxis=dict(gridcolor="rgba(27,67,50,0.1)"),
            )
            st.plotly_chart(_tema_fig(fig, height=220), use_container_width=True)

    # ── FILTER FORM ─────────────────────────────────────────────────────────
    if "tm_ta" not in st.session_state:
        st.session_state.tm_ta = topik[0]
    if "tm_tb" not in st.session_state:
        st.session_state.tm_tb = topik[min(1, len(topik) - 1)]

    def _safe_idx(nama):
        return topik.index(nama) if nama in topik else 0

    with st.form("filter_topik_form"):
        fc1, fc2, fc3 = st.columns([2, 2, 1])
        sel_a = fc1.selectbox("Topik A", topik, index=_safe_idx(st.session_state.tm_ta))
        sel_b = fc2.selectbox("Topik B", topik, index=_safe_idx(st.session_state.tm_tb))
        if fc3.form_submit_button("Apply"):
            st.session_state.tm_ta = sel_a
            st.session_state.tm_tb = sel_b

    topik_a = st.session_state.tm_ta
    topik_b = st.session_state.tm_tb

    if topik_a == topik_b:
        st.warning("Pilih dua topik yang berbeda.")

    ring_a = ringkasan_topik(gabung, topik_a)
    ring_b = ringkasan_topik(gabung, topik_b)
    ada_shares = ring_a["shares"] is not None

    # ── KPI GRUP ────────────────────────────────────────────────────────────
    def _pendek(nama, maks=15):
        return nama if len(nama) <= maks else nama[:maks - 1] + "…"

    n_grup = 4 if ada_shares else 3
    kpi_cols = st.columns(n_grup)
    kpi_items = [
        ("Jumlah Komentar",   _KPI["komentar"], ring_a["komentar"], ring_b["komentar"]),
        ("Rata-rata Likes",   _KPI["likes"],    ring_a["likes"],    ring_b["likes"]),
        ("Rata-rata Replies", _KPI["replies"],  ring_a["replies"],  ring_b["replies"]),
    ]
    if ada_shares:
        kpi_items.append(
            ("Rata-rata Shares", _KPI["shares"], ring_a["shares"], ring_b["shares"])
        )

    for col, (label, warna_kpi, val_a, val_b) in zip(kpi_cols, kpi_items):
        _kpi_grup(col, label, warna_kpi,
                  _pendek(topik_a), val_a,
                  _pendek(topik_b), val_b)

    # ── BARIS BAWAH: Time series (kiri) + Lambda + Kata (kanan) ─────────────
    col_ts, col_kata = st.columns([1.2, 1])

    with col_ts:
        with st.container(border=True):
            st.markdown(
                f"<p style='font-weight:700;color:{config.COLORS['text_dark']};margin:0 0 4px 0;'>"
                "Tren Jumlah Komentar per Hari</p>",
                unsafe_allow_html=True,
            )
            ts = (gabung[gabung["topic_name"].isin([topik_a, topik_b])]
                  .dropna(subset=["date"])
                  .assign(tanggal=lambda d: d["date"].dt.normalize())
                  .groupby(["tanggal", "topic_name"]).size()
                  .reset_index(name="jumlah"))
            if ts.empty:
                st.info("Tidak ada data untuk dua topik ini.")
            else:
                fig = px.line(ts, x="tanggal", y="jumlah", color="topic_name",
                              color_discrete_map=warna,
                              labels={"tanggal": "", "jumlah": "Komentar",
                                      "topic_name": "Topik"})
                fig.update_layout(
                    legend_title_text="",
                    xaxis=dict(gridcolor="rgba(27,67,50,0.1)"),
                    yaxis=dict(gridcolor="rgba(27,67,50,0.1)"),
                )
                st.plotly_chart(_tema_fig(fig, height=250,
                                          margin=dict(l=5, r=5, t=10, b=5)),
                                use_container_width=True)

    with col_kata:
        with st.container(border=True):
            if comparison is not None:
                st.markdown(
                    f"<p style='font-size:0.82rem;color:{config.COLORS['text_dark']};margin:0 0 4px 0;'>"
                    "<b>λ (lambda):</b> mendekati <b>1</b> → kata paling sering di topik; "
                    "mendekati <b>0</b> → kata paling khas/eksklusif topik itu.</p>",
                    unsafe_allow_html=True,
                )
                lam = st.slider("λ", 0.0, 1.0, 0.6, 0.1)
            else:
                lam = 1.0
                st.markdown(
                    f"<p style='font-size:0.82rem;color:{config.COLORS['muted']};'>"
                    "Filter lambda tidak tersedia (topic_comparison.csv belum ada).</p>",
                    unsafe_allow_html=True,
                )

            kk1, kk2 = st.columns(2)
            with kk1:
                fig_a = _bar_kata(words, comparison, nama_ke_id[topik_a],
                                  lam, topik_a, warna[topik_a])
                st.plotly_chart(fig_a, use_container_width=True)
            with kk2:
                fig_b = _bar_kata(words, comparison, nama_ke_id[topik_b],
                                  lam, topik_b, warna[topik_b])
                st.plotly_chart(fig_b, use_container_width=True)
