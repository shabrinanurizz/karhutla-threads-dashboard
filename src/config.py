"""Konfigurasi global dashboard (satu-satunya sumber design system dan path).

Semua halaman dan modul mengambil warna, font, path, dan daftar navigasi dari
file ini. Ubah nilai di sini agar perubahan berlaku ke seluruh dashboard.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Path (terpusat)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_PATH = ASSETS_DIR / "style.css"
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_OUTPUT_DIR = BASE_DIR / "data" / "model_output"

# Nama file dataset (None = ambil file .csv/.xlsx pertama di foldernya).
RAW_DATA_FILE = "comments_raw.csv"
PROCESSED_DATA_FILE = "comments_clean.csv"

# Pemetaan kolom dataset (sesuai header file di data/raw dan data/processed).
COLUMNS = {
    "id": "comment_id",
    "user": "user_id",
    "date": "date",
    "text": "comment_text",
    "likes": "likes",
    "shares": "shares",
    "replies": "replies",
    "text_clean": "text_clean",
}

# Gambar ilustrasi Overview (opsional). Jika file tidak ada, placeholder tampil.
FOREST_IMAGE = ASSETS_DIR / "forest.png"

# ---------------------------------------------------------------------------
# Identitas aplikasi (PLACEHOLDER: ganti dengan teks final)
# ---------------------------------------------------------------------------
APP_NAME = "Dashboard Karhutla"
APP_DESCRIPTION = "Dashboard interaktif analisis komentar media sosial terkait kebakaran hutan dan lahan (karhutla)."
APP_ICON = "🔥"
SIDEBAR_TITLE = "DASHBOARD KARHUTLA"  # sesuai referensi desain

PROJECT_TITLE = "DASHBOARD ANALISIS KOMENTAR THREADS MENGENAI KARHUTLA"
BACKGROUND_TEXT = "[Placeholder] Isi latar belakang proyek di sini."
OBJECTIVE_TEXT = "[Placeholder] Isi tujuan proyek di sini."

GROUP_IDENTITY = {
    "course": "STA1381 - Pengantar Sains Data",
    "lecturer": "Septian Rahardiantoro S.Stat., M.Si., Ph.D.",
    "members": ["Muhammad Ayyash S.| M0401241001",
                "Daffa Lukman W. A. J. | M0401241008",
                "Shabrina Nur Izzati | M0401241011",
                "Najwa Salsabila M.N | M0401241016",
                "Uma Keisha Abriana  | M0401241022",
                "Naurah Aathirah Farid | M0401241037"
                ],  # placeholder
}

# Langkah alur analisis (label, ikon, varian warna). Sesuai referensi Overview.
WORKFLOW_STEPS = [
    ("Scraping Data Threads", "⬇️", "dark"),
    ("Cleaning & Case Folding", "🧹", "red"),
    ("Stopword Removal", "🚫", "orange"),
    ("Stemming", "🌱", "dark"),
    ("Tokenisasi", "✂️", "red"),
    ("Eksplorasi", "🔍", "orange"),
    ("Co-occurrence & Korelasi", "🕸️", "dark"),
    ("LDA Topic Modelling", "💡", "red"),
] # Ini nanti pake visualisasi aja entar dimasukin ke assets

# ---------------------------------------------------------------------------
# Navigasi: file halaman, label sidebar, ikon material
# ---------------------------------------------------------------------------
PAGES = [
    {"path": "pages/1_Overview.py", "label": "OVERVIEW", "icon": ":material/bookmark:"},
    {"path": "pages/2_EDA.py", "label": "EDA", "icon": ":material/bar_chart:"},
    {"path": "pages/3_Cooccurrence.py", "label": "CO-OCCURANCE ANALYSIS", "icon": ":material/hub:"},
    {"path": "pages/4_Topic_Analysis.py", "label": "MODELLING", "icon": ":material/lightbulb:"},
    {"path": "pages/5_Comment_Explorer.py", "label": "COMMENT EXPLORER", "icon": ":material/search:"},
    {"path": "pages/6_Insights_Conclusion.py", "label": "INSIGHT & KESIMPULAN", "icon": ":material/error:"},
]

# ---------------------------------------------------------------------------
# Design system (diturunkan dari 5 gambar referensi; hex adalah perkiraan)
# ---------------------------------------------------------------------------
COLORS = {
    "green_dark": "#1B4332",
    "red_orange": "#D94A05",
    "orange": "#E85D10",
    "amber": "#F58E0A",
    "cream": "#F5F0E6",
    "cream_light": "#FDF9EE",
    "text_dark": "#1B4332",
    "text_light": "#FFFFFF",
    "muted": "#8A8F86",
    "gold": "#C9963F",
}

# Varian kartu/KPI -> warna latar
VARIANT_COLORS = {
    "dark": COLORS["green_dark"],
    "red": COLORS["red_orange"],
    "orange": COLORS["amber"],
}

# Urutan warna kategori untuk chart (pertama = ijo tua untuk kontras pada latar cream)
CHART_COLORWAY = [
    COLORS["green_dark"],
    COLORS["orange"],
    COLORS["amber"],
    COLORS["gold"],
    "#2D6A4F",
    "#95A5A6",
    "#B8B8B8",
]

FONT_FAMILY = "Montserrat"
FONT_URL = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap"

LAYOUT = {
    "page_layout": "wide",
    "card_radius": "8px",
    "chart_height": 380,
}

CHART = {
    "font_family": f"{FONT_FAMILY}, sans-serif",
    "font_color": COLORS["text_dark"],
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 10, "r": 10, "t": 40, "b": 10},
}

EMPTY_VALUE = "—"

