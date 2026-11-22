
import streamlit as st

from src.visualization import (
    render_page_title,
    render_section_header,
    render_info_card,
    render_data_notice,
)


def render():
    render_page_title("INSIGHT & KESIMPULAN")

    # =========================================================
    # KEY INSIGHTS
    # =========================================================
    render_section_header(
        "Key Insights",
    )

    render_info_card(
        "Key Insights",
        "Insight utama dari EDA, Co-occurrence, Topic Modeling, "
        "dan analisis lainnya akan ditampilkan di bagian ini "
        "berdasarkan hasil analisis aktual.",
    )

    st.divider()

    # =========================================================
    # KESIMPULAN DAN SARAN
    # =========================================================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_section_header("Kesimpulan")
        render_info_card(
            "Kesimpulan Analisis",
            "Kesimpulan menyeluruh mengenai pola, tren, "
            "dan temuan dari hasil analisis data akan "
            "ditempatkan di sini.dan temuan dari hasil analisis data akan "
            "ditempatkan di sini.dan temuan dari hasil analisis data akan "
            "ditempatkan di sini.",
        )

    with col2:
        render_section_header("Rekomendasi")
        render_info_card(
            "Rekomendasi",
            "Saran dan rekomendasi berdasarkan hasil analisis "
            "akan dituliskan di bagian ini.Saran dan rekomendasi berdasarkan hasil analisis "
            "akan dituliskan di bagian ini.Saran dan rekomendasi berdasarkan hasil analisis "
            "akan dituliskan di bagian ini.Saran dan rekomendasi berdasarkan hasil analisis "
            "akan dituliskan di bagian ini.",
        )


render()
