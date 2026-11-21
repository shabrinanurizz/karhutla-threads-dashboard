"""Halaman 4 - Topic Analysis. Tampilan saja; logika ada di src/topic_modeling.py."""
import streamlit as st

from src.data_loader import load_processed_data
from src import config
from src.topic_modeling import (
    show_topic_analysis,
    load_topic_assignments,
    load_topic_words,
    load_topic_metrics,
    load_topic_comparison,
)

data = load_processed_data()
if data is None:
    st.error("Data belum tersedia. Pastikan data/processed/comments_clean.csv ada.")
    st.stop()

text_col = config.COLUMNS["text_clean"]
if text_col not in data.columns:
    st.error(f"Kolom '{text_col}' tidak ditemukan dalam dataset.")
    st.stop()

try:
    topics = load_topic_assignments()
    words = load_topic_words()
    metrics = load_topic_metrics()
    try:
        comparison = load_topic_comparison()
    except FileNotFoundError:
        comparison = None
except FileNotFoundError as e:
    st.error(f"{e}\n\nPastikan file hasil topic modeling ada di data/model_output/.")
    st.stop()

show_topic_analysis(data, topics, words, metrics, comparison)
