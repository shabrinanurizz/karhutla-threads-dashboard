import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analisis Topik", layout="wide")

# ---------- DATA DUMMY (nanti diganti CSV hasil model) ----------
rng = np.random.default_rng(42)
topik = ["Dampak Asap", "Kebakaran Lahan", "Penanganan"]
tanggal = pd.date_range("2026-08-02", "2026-08-31")
komentar = pd.DataFrame({
    "tanggal": rng.choice(tanggal, 500),
    "topic_name": rng.choice(topik, 500, p=[0.4, 0.35, 0.25]),
    "likes": rng.integers(0, 50, 500),
    "shares": rng.integers(0, 10, 500),
    "replies": rng.integers(0, 15, 500),
})
kata = pd.DataFrame({
    "topic_name": ["Dampak Asap"] * 5 + ["Kebakaran Lahan"] * 5 + ["Penanganan"] * 5,
    "word": ["asap", "sesak", "masker", "ispa", "yang",
             "lahan", "bakar", "sawit", "gambut", "yang",
             "pemadam", "hujan", "bantuan", "tim", "yang"],
    "p_topik": [0.08, 0.04, 0.035, 0.03, 0.06,
                0.07, 0.06, 0.04, 0.03, 0.055,
                0.05, 0.04, 0.035, 0.03, 0.05],
    "p_korpus": [0.05, 0.01, 0.008, 0.004, 0.07,
                 0.04, 0.03, 0.01, 0.006, 0.07,
                 0.01, 0.012, 0.01, 0.01, 0.07],
})

# ---------- GAYA ----------
WARNA = {"Dampak Asap": "#4C78A8", "Kebakaran Lahan": "#E45756", "Penanganan": "#54A24B"}

def rapikan(fig, tinggi=320):
    fig.update_layout(height=tinggi, margin=dict(l=10, r=10, t=50, b=10),
                      legend_title_text="")
    return fig

# ---------- HEADER (dipadatkan) ----------
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
        st.plotly_chart(rapikan(fig, 400), use_container_width=True)
    with kanan:
        st.metric("Coherence Score", "0.52", border=True)  # dummy
        st.metric("Jumlah Topik", len(topik), border=True)
        st.metric("Total Komentar", len(komentar), border=True)

# ---------- TAB 2 ----------
def tampil_topik(nama):
    with st.container(border=True):
        st.markdown(f"**{nama}**")
        d = komentar[komentar["topic_name"] == nama]
        k = st.columns(4)
        k[0].metric("Komentar", len(d))
        k[1].metric("Likes", round(d["likes"].mean(), 1))
        k[2].metric("Shares", round(d["shares"].mean(), 1))
        k[3].metric("Replies", round(d["replies"].mean(), 1))

        w = kata[kata["topic_name"] == nama].copy()
        rel = lam * np.log(w["p_topik"]) + (1 - lam) * np.log(w["p_topik"] / w["p_korpus"])
        w["skor"] = (rel - rel.min()) / (rel.max() - rel.min() + 1e-9)
        w = w.sort_values("skor")
        fig = px.bar(w, x="skor", y="word", orientation="h",
                     title="Top Kata", labels={"skor": "Skor relevansi", "word": ""})
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
                  .groupby(["tanggal", "topic_name"]).size().reset_index(name="jumlah"))
            fig = px.line(ts, x="tanggal", y="jumlah", color="topic_name",
                          color_discrete_map=WARNA, title="Komentar per Hari",
                          labels={"tanggal": "", "jumlah": "Komentar"})
            st.plotly_chart(rapikan(fig, 400), use_container_width=True)
    with kolB:
        tampil_topik(topik_b)