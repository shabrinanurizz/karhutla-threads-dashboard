"""Halaman 4 - Topic Analysis. Tampilan saja; logika ada di src/topic_modeling.py."""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.topic_modeling import (
    show_topic_analysis,
    load_topic_assignments,
    load_topic_words,
    load_topic_metrics,
    load_topic_comparison,
)

st.set_page_config(page_title="Analisis Topik", layout="wide")

# SEMENTARA: ganti dengan load_comments() dari src/data_loader.py (Anggota 2)
# bila fungsi itu sudah ada. Kolom file ini sudah sesuai kontrak
# (comment_id, user_id, date, comment_text, likes, shares, replies, text_clean).
FILE_KOMENTAR = (Path(__file__).resolve().parent.parent
                 / "data" / "processed" / "comments_clean.csv")


@st.cache_data
def muat_semua():
    data = pd.read_csv(FILE_KOMENTAR)
    topics = load_topic_assignments()
    words = load_topic_words()
    metrics = load_topic_metrics()
    try:
        comparison = load_topic_comparison()
    except FileNotFoundError:
        comparison = None
    return data, topics, words, metrics, comparison


try:
    data, topics, words, metrics, comparison = muat_semua()
except FileNotFoundError as e:
    st.error(f"{e}\n\nPastikan data/processed/comments_clean.csv ada (data dari Anggota 2).")
    st.stop()

show_topic_analysis(data, topics, words, metrics, comparison)
