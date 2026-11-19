"""Komponen visualisasi reusable lintas halaman.

Contoh pemakaian di halaman mana pun:

    from src.visualization import render_kpi, render_bar_chart, render_section_header

    render_section_header("Judul Halaman")
    render_kpi("Total Komentar", 1234, variant="dark")
    render_bar_chart(df, x="kata", y="jumlah", title="Top Kata", horizontal=True)

Semua gaya (warna, font, radius) diambil dari `src/config.py`.
"""

from html import escape

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud

from src import config
from src.utils import format_number


# ---------------------------------------------------------------------------
# Helper internal
# ---------------------------------------------------------------------------
def _style_figure(fig, title=None, height=None):
    """Terapkan tema chart global ke figure Plotly."""
    fig.update_layout(
        title={"text": title, "font": {"size": 20, "color": config.COLORS["text_dark"]}} if title else None,
        font={"family": config.CHART["font_family"], "color": config.CHART["font_color"]},
        paper_bgcolor=config.CHART["paper_bgcolor"],
        plot_bgcolor=config.CHART["plot_bgcolor"],
        margin=config.CHART["margin"],
        height=height or config.LAYOUT["chart_height"],
        colorway=config.CHART_COLORWAY,
    )
    return fig


def _show(fig, key=None):
    """Tampilkan figure Plotly dengan lebar penuh."""
    st.plotly_chart(fig, use_container_width=True, key=f"chart_{key or 'default'}", config={"displaylogo": False})


def _is_empty(data):
    return data is None or len(data) == 0


def _empty_notice(title):
    render_data_notice(f"Data untuk “{title}” belum tersedia.")


# ---------------------------------------------------------------------------
# Teks dan kartu
# ---------------------------------------------------------------------------
def render_page_title(title, accent=False):
    """Judul halaman besar (kapital, tebal). accent=True memakai warna oranye (Overview)."""
    css = "page-title accent" if accent else "page-title"
    st.markdown(f"<h1 class='{css}'>{escape(title)}</h1>", unsafe_allow_html=True)


def render_section_header(title, description=None):
    """Judul section dengan deskripsi opsional. Jika title kosong/None, tidak render apa-apa."""
    if not title:
        return
    html = f"<div class='section-header'><h3>{escape(title)}</h3>"
    if description:
        html += f"<p>{escape(description)}</p>"
    st.markdown(html + "</div>", unsafe_allow_html=True)


def render_kpi(
    title,
    value,
    delta=None,
    variant="dark",
    compact=False,
    width=None,
    height=None,
    value_size="3.6rem",
    title_size="1rem",
    title_line_height="1.2",
    title_margin="4px",
    padding="22px 12px",
):
    """KPI card dengan ukuran dan typography fleksibel."""

    shown = value if isinstance(value, str) else format_number(value)

    delta_html = (
        f"<div class='kpi-delta'>{escape(str(delta))}</div>"
        if delta else ""
    )
    shown_html = escape(str(shown)).replace("\n", "<br>")
    size = " kpi-compact" if compact else ""

    custom_style = ""
    if width:
        custom_style += f"width: {width};"
    if height:
        custom_style += f"height: {height};"

    custom_style += f"padding: {padding};"

    st.markdown(
        f"<div class='kpi-card kpi-{variant}{size}' "
        f"style='{custom_style}'>"
        f"<div class='kpi-value' "
        f"style='font-size:{value_size};'>{shown_html}</div>"
        f"<div class='kpi-title' "
        f"style='font-size:{title_size};"
        f"line-height:{title_line_height};"
        f"margin-top:{title_margin};'>"
        f"{escape(str(title))}</div>"
        f"{delta_html}</div>",
        unsafe_allow_html=True,
    )


def render_info_card(title, content, variant="light"):
    """Kartu teks. variant: "light" (krem terang) atau "dark" (hijau)."""
    st.markdown(
        f"<div class='info-card info-{variant}'><h4>{escape(title)}</h4>"
        f"<p>{escape(content)}</p></div>",
        unsafe_allow_html=True,
    )


def render_banner(left, right):
    """Banner hijau berisi dua kartu putih. `left`/`right` = (judul, isi)."""
    cards = "".join(
        f"<div class='info-card info-light'><h4>{escape(t)}</h4><p>{escape(c)}</p></div>"
        for t, c in (left, right)
    )
    st.markdown(f"<div class='banner'>{cards}</div>", unsafe_allow_html=True)


def render_pill_label(text, variant="dark"):
    """Label pill berwarna (dark/red/orange), mis. header grup KPI. Jika text kosong/None, tidak render."""
    if not text:
        return
    st.markdown(f"<div class='pill-label pill-{variant}'>{escape(text)}</div>", unsafe_allow_html=True)


def render_badge(text, variant="red"):
    """HTML badge kecil (untuk tabel), dikembalikan sebagai string."""
    return f"<span class='badge badge-{variant}'>{escape(text)}</span>"


def render_data_notice(message, level="info"):
    """Pesan jelas bila data/fitur belum tersedia. level: info | warning."""
    css = "notice-warning" if level == "warning" else "notice-info"
    st.markdown(f"<div class='notice {css}'>{escape(message)}</div>", unsafe_allow_html=True)


def render_placeholder_card(title, message="Placeholder: konten akan diisi kemudian."):
    """Kartu kosong berlabel untuk area yang belum diimplementasikan."""
    st.markdown(
        f"<div class='info-card info-light placeholder'><h4>{escape(title)}</h4>"
        f"<p>{escape(message)}</p></div>",
        unsafe_allow_html=True,
    )


def render_process_flow(steps, title=None):
    """Panel alur proses. `steps` = list (label, ikon, variant) seperti config.WORKFLOW_STEPS."""
    tiles = "".join(
        f"<div class='flow-step flow-{variant}'><div class='flow-icon'>{icon}</div>"
        f"<div class='flow-label'>{escape(label)}</div></div>"
        for label, icon, variant in steps
    )
    heading = f"<h3>{escape(title)}</h3>" if title else ""
    st.markdown(f"<div class='flow-panel'>{heading}<div class='flow-grid'>{tiles}</div></div>",
                unsafe_allow_html=True)

def render_sidebar_identity(identity=None):
    """Kartu 'Identitas Kelompok' untuk sidebar."""
    identity = identity or config.GROUP_IDENTITY
    members = "".join(f"<div class='member-pill'>{escape(m)}</div>" for m in identity["members"])
    st.markdown(
        "<div class='identity-card'><h5>IDENTITAS KELOMPOK</h5>"
        f"<div>Matkul: {escape(identity['course'])}</div>"
        f"<div>Dosen: {escape(identity['lecturer'])}</div>{members}</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------
def render_bar_chart(data, x, y, title=None, horizontal=False, color=None,
                     color_sequence=None, show_values=True, height=None, key=None):
    """Bar chart.

    Args:
        data: DataFrame.
        x, y: Nama kolom. Untuk horizontal=True, `y` = kategori dan `x` = nilai.
        horizontal: Bar horizontal (gaya Top 10 pasangan kata); urutan teratas di atas.
        color: Kolom untuk pewarnaan kategori (opsional).
        color_sequence: List warna; jika None memakai palet global.
        show_values: Tampilkan label nilai di ujung bar.
    """
    if _is_empty(data):
        return _empty_notice(title or "Bar chart")
    fig = px.bar(
        data, x=x, y=y, color=color,
        orientation="h" if horizontal else "v",
        color_discrete_sequence=color_sequence or config.CHART_COLORWAY,
        text=(x if horizontal else y) if show_values else None,
    )
    if show_values:
        fig.update_traces(textposition="outside", cliponaxis=False)
    if horizontal:
        fig.update_yaxes(autorange="reversed", title=None)
        fig.update_xaxes(visible=False)
    fig.update_layout(showlegend=color is not None)
    _show(_style_figure(fig, title, height), key)


def render_line_chart(data, x, y, title=None, color=None, markers=True, height=None, key=None):
    """Line chart (tren waktu, skor koherens, dll.)."""
    if _is_empty(data):
        return _empty_notice(title or "Line chart")
    fig = px.line(data, x=x, y=y, color=color, markers=markers,
                  color_discrete_sequence=config.CHART_COLORWAY)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(27,67,50,0.1)")
    _show(_style_figure(fig, title, height), key)


def render_pie_chart(data, names, values, title=None, hole=0.0, height=None, key=None):
    """Pie chart. Gunakan `hole` (0-1) untuk gaya donut."""
    if _is_empty(data):
        return _empty_notice(title or "Pie chart")
    fig = px.pie(data, names=names, values=values, hole=hole,
                 color_discrete_sequence=config.CHART_COLORWAY)
    fig.update_traces(textinfo="label+percent", sort=False)
    _show(_style_figure(fig, title, height), key)


def render_donut_chart(data, names, values, title=None, height=None, key=None):
    """Donut chart (pie dengan lubang)."""
    render_pie_chart(data, names, values, title, hole=0.55, height=height, key=key)


def render_histogram(data, x, title=None, nbins=None, height=None, key=None):
    """Histogram distribusi satu kolom numerik."""
    if _is_empty(data):
        return _empty_notice(title or "Histogram")
    fig = px.histogram(data, x=x, nbins=nbins, color_discrete_sequence=[config.COLORS["red_orange"]])
    fig.update_layout(bargap=0.05)
    _show(_style_figure(fig, title, height), key)


def render_heatmap(data, x, y, z, title=None, height=None, key=None):
    """Heatmap dari DataFrame long-format (kolom x, y, z)."""
    if _is_empty(data):
        return _empty_notice(title or "Heatmap")
    pivot = data.pivot_table(index=y, columns=x, values=z, aggfunc="sum")
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0, config.COLORS["cream_light"]], [0.5, config.COLORS["amber"]],
                    [1, config.COLORS["green_dark"]]],
    ))
    _show(_style_figure(fig, title, height), key)
    _show(_style_figure(fig, title, height), key)


def render_wordcloud(data, text_col, title=None, height=None, key=None):
    """Render WordCloud dari kolom teks menggunakan library `wordcloud`.

    Args:
        data: DataFrame yang berisi kolom teks.
        text_col: Nama kolom teks (mis. "comment_text").
        title: Judul chart (opsional).
        height: Tinggi figure (opsional).
        key: Streamlit key (opsional).
    """
    if _is_empty(data) or text_col not in data.columns:
        return _empty_notice(title or "WordCloud")

    teks = " ".join(data[text_col].astype(str).fillna("").tolist())
    if not teks.strip():
        return _empty_notice(title or "WordCloud")

    wc = WordCloud(
        width=800,
        height=400,
        background_color=config.COLORS["cream_light"],
        colormap="autumn",
        max_words=100,
        collocations=False,
    ).generate(teks)

    fig_w, fig_h = plt.subplots(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if title:
        plt.title(title, fontsize=16, color=config.COLORS["text_dark"], fontweight="bold", pad=20)
    plt.tight_layout()
    st.pyplot(fig_w, use_container_width=True)
    plt.close(fig_w)

