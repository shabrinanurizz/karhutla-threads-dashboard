import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Analisis Topik", layout="wide")

# ---------- MUAT DATA ----------
DATA = Path(__file__).resolve().parent.parent / "data"
FILE_KOMENTAR = DATA / "raw" / "data karhutla gabungan terbaru.csv"   # <- ganti ke data final nanti

@st.cache_data
def muat_data():
    asg = pd.read_csv(DATA / "model_output" / "topic_assignments.csv")
    kata = pd.read_csv(DATA / "model_output" / "topic_words.csv")
    metrics = pd.read_csv(DATA / "model_output" / "topic_metrics.csv")
    raw = pd.read_csv(FILE_KOMENTAR).rename(columns={
        "comment_code": "comment_id", "like_count": "likes", "reply_count": "replies"})
    komentar = asg.merge(raw[["comment_id", "tanggal", "likes", "replies"]],
                         on="comment_id", how="left")
    komentar["tanggal"] = pd.to_datetime(komentar["tanggal"])
    return komentar, kata, metrics

try:
    komentar, kata, metrics = muat_data()
except FileNotFoundError as e:
    st.error(f"File data tidak ditemukan: {e.filename}")
    st.stop()

topik = kata.drop_duplicates("topic_id").sort_values("topic_id")["topic_name"].tolist()

# ---------- GAYA ----------
PALET = ["#4C78A8", "#E45756", "#54A24B", "#F58518", "#B279A2", "#72B7B2"]
WARNA = dict(zip(topik, PALET))

def rapikan(fig, tinggi=320):
    fig.update_layout(height=tinggi, margin=dict(l=10, r=10, t=50, b=10),
                      legend_title_text="")
    return fig

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 0.5rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("### Analisis Topik")
tab1, tab2 = st.tabs(["Gambaran Umum", "Perbandingan Topik"])

# ---------- TAB 1 ----------
with tab1:
    kiri, kanan = st.columns([2, 1])
    with kiri.container(border=True):
        proporsi = komentar["topic_name"].value_counts().reset_index()
        proporsi.columns = ["topik", "jumlah"]
        fig = px.pie(proporsi, names="topik", values="jumlah", hole=0.45,
                     color="topik", color_discrete_map=WARNA,
                     title="Proporsi Komentar per Topik")
        st.plotly_chart(rapikan(fig, 420), use_container_width=True)
    with kanan:
        skor = metrics.loc[metrics["jumlah_topik"] == len(topik), "coherence"].iloc[0]
        st.metric(f"Coherence Score (K = {len(topik)})", round(skor, 3), border=True)
        st.metric("Total Komentar", len(komentar), border=True)
        with st.container(border=True):
            fig = px.line(metrics, x="jumlah_topik", y="coherence", markers=True,
                          title="Coherence per Jumlah Topik",
                          labels={"jumlah_topik": "Jumlah topik", "coherence": "Coherence"})
            st.plotly_chart(rapikan(fig, 230), use_container_width=True)

# ---------- TAB 2 ----------
def tampil_topik(nama):
    with st.container(border=True):
        st.markdown(f"**{nama}**")
        d = komentar[komentar["topic_name"] == nama]
        k = st.columns(3)
        k[0].metric("Komentar", len(d))
        k[1].metric("Rata2 Likes", round(d["likes"].mean(), 1))
        k[2].metric("Rata2 Replies", round(d["replies"].mean(), 1))

        w = kata[kata["topic_name"] == nama].copy()
        rel = lam * np.log(w["p_topik"]) + (1 - lam) * np.log(w["p_topik"] / w["p_korpus"])
        w["skor"] = (rel - rel.min()) / (rel.max() - rel.min() + 1e-9)
        w = w.nlargest(10, "skor").sort_values("skor")
        fig = px.bar(w, x="skor", y="word", orientation="h",
                     title="Top 10 Kata", labels={"skor": "Skor relevansi", "word": ""})
        fig.update_traces(marker_color=WARNA[nama])
        st.plotly_chart(rapikan(fig, 250), use_container_width=True)

with tab2:
    f1, f2, f3 = st.columns(3)
    topik_a = f1.selectbox("Topik A", topik, index=0)
    topik_b = f2.selectbox("Topik B", topik, index=1)
    lam = f3.slider("Lambda (λ)", 0.0, 1.0, 0.6, 0.1,
                    help="1 = kata paling sering di topik, 0 = kata paling khas topik")
    if topik_a == topik_b:
        st.warning("Pilih dua topik yang berbeda.")

    kolA, kolTS, kolB = st.columns([1, 1.2, 1])
    with kolA:
        tampil_topik(topik_a)
    with kolTS:
        with st.container(border=True):
            ts = (komentar[komentar["topic_name"].isin([topik_a, topik_b])]
                  .dropna(subset=["tanggal"])
                  .groupby(["tanggal", "topic_name"]).size().reset_index(name="jumlah"))
            fig = px.line(ts, x="tanggal", y="jumlah", color="topic_name",
                          color_discrete_map=WARNA, title="Komentar per Hari",
                          labels={"tanggal": "", "jumlah": "Komentar"})
            st.plotly_chart(rapikan(fig, 400), use_container_width=True)
    with kolB:
        tampil_topik(topik_b)