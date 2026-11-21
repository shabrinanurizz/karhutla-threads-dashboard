"""Halaman Insights & Conclusion (kerangka — isi final belum ditentukan).

Halaman ini menampung rangkuman insight dan kesimpulan dari seluruh analisis
dashboard (EDA, Co-occurrence, Topic Modeling, dan lain-lain). Saat ini hanya
berisi placeholder berbasis layout fleksibel; tidak ada hasil analisis atau
kesimpulan yang dipersiapkan secara buatan.

Struktur dirancang agar dapat diperbarui tanpa mengubah fondasi aplikasi:
setiap insight ditempatkan di kartu tersendiri yang dapat diisi konten final
nanti secara independen.
"""

import streamlit as st

from src import config
from src.visualization import (
    render_page_title,
    render_section_header,
    render_info_card,
    render_data_notice,
)


def render():
    render_page_title("INSIGHT & KESIMPULAN")

    render_section_header(
        "Rangkuman Hasil Analisis",
        "Halaman ini akan diisi dengan insight utama, temuan penting, dan "
        "kesimpulan setelah seluruh halaman analisis (Tahap 4) selesai "
        "diimplementasikan dengan dataset aktual.",
    )

    # ------------------------------------------------------------------
    # Layout fleksibel: 3 kolom untuk insight utama / temuan / kesimpulan
    # ------------------------------------------------------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        render_section_header("Insight Utama")
        render_info_card(
            "Placeholder",
            "Insight utama dari analisis akan ditempatkan di sini. "
            "Isi final akan ditentukan setelah data dan analisis tersedia.",
        )

    with c2:
        render_section_header("Temuan Penting")
        render_info_card(
            "Placeholder",
            "Temuan penting dari EDA, Co-occurrence, dan Topic Modeling "
            "dirangkum di sini.",
        )

    with c3:
        render_section_header("Kesimpulan")
        render_info_card(
            "Placeholder",
            "Kesimpulan keseluruhan dashboard akan dituliskan di sini "
            "berdasarkan hasil analisis yang tersedia.",
        )

    st.divider()

    # ------------------------------------------------------------------
    # Area integrasi hasil analisis (fleksibel untuk dikembangkan ke depan)
    # ------------------------------------------------------------------
    render_section_header("Integrasi Hasil Analisis Lainnya")
    render_info_card(
        "Catatan pengembang",
        "Tempatkan ringkasan visual atau ringkasan numerik dari halaman "
        "EDA, Co-occurrence, Topic Modeling, dan Comment Explorer di area "
        "ini. Layout kolom di atas dapat diperluas atau diubah tanpa mengubah "
        "fondasi aplikasi di app.py.",
    )

    render_data_notice(
        "Catatan: semua konten di halaman ini adalah placeholder. Jangan mengarang "
        "hasil analisis atau kesimpulan sebelum instruksi berikutnya diberikan.",
        level="info",
    )


render()

