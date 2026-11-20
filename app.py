import streamlit as st

from src import config
from src.utils import load_css
from src.visualization import render_sidebar_identity

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout=config.LAYOUT["page_layout"],
    initial_sidebar_state="expanded",
)

# Muat CSS design system sekali di entry point.
load_css()

# Branding sidebar (judul + identitas kelompok) tampil di atas daftar navigasi.
st.sidebar.markdown(
    f"<div class='sidebar-title'>{config.SIDEBAR_TITLE}</div>",
    unsafe_allow_html=True,
)
with st.sidebar:
    render_sidebar_identity()

# Daftar halaman navigasi (6 halaman), diurutkan sesuai config.PAGES.
pages = [
    st.Page(
        page["path"],
        title=page["label"],
        icon=page.get("icon"),
        default=(i == 0),
    )
    for i, page in enumerate(config.PAGES)
]

pg = st.navigation(pages)
pg.run()

