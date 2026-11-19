# Development Guide

Panduan lengkap untuk mengedit, mengembangkan, dan menambahkan fitur pada setiap halaman dalam project **Karhutla Threads Dashboard**. Dokumen ini ditulis untuk developer, termasuk pemula yang baru mengenal project ini. Semua penjelasan, nama file, nama fungsi, dan parameter diturunkan langsung dari implementasi aktual (tidak bersifat generik).

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Project Architecture](#2-project-architecture)
- [3. Global Configuration](#3-global-configuration)
- [4. Global Styling System](#4-global-styling-system)
- [5. Page-by-Page Editing Guide](#5-page-by-page-editing-guide)
  - [5.1 Halaman 1 — Overview (`pages/1_Overview.py`)](#51-halaman-1---overview-pages1_overviewpy)
  - [5.2 Halaman 2 — EDA (`pages/2_EDA.py`)](#52-halaman-2---eda-pages2_edapy)
  - [5.3 Halaman 3 — Co-occurrence Analysis (`pages/3_Cooccurrence.py`)](#53-halaman-3---co-occurrence-analysis-pages3_cooccurrencepy)
  - [5.4 Halaman 4 — Topic Analysis / Modelling (`pages/4_Topic_Analysis.py`)](#54-halaman-4---topic-analysis--modelling-pages4_topic_analysispy)
  - [5.5 Halaman 5 — Comment Explorer (`pages/5_Comment_Explorer.py`)](#55-halaman-5---comment-explorer-pages5_comment_explorerpy)
  - [5.6 Halaman 6 — Insight & Kesimpulan (`pages/6_Insights_Conclusion.py`)](#56-halaman-6---insight--kesimpulan-pages6_insights_conclusionpy)
- [6. Topic Modelling Module](#6-topic-modelling-module)
- [7. Analytics Module](#7-analytics-module)
- [8. Other Modules](#8-other-modules)
- [9. How to Add a New Page](#9-how-to-add-a-new-page)
- [10. How to Add a New Feature](#10-how-to-add-a-new-feature)
- [11. Custom Design Without Global Styling](#11-custom-design-without-global-styling)
- [12. Missing Components and Recommendations](#12-missing-components-and-recommendations)
- [13. Troubleshooting](#13-troubleshooting)
- [14. Development Workflow](#14-development-workflow)

---

## 1. Project Overview

**Karhutla Threads Dashboard** adalah aplikasi interaktif berbasis **Streamlit** untuk menganalisis komentar media sosial (Threads) terkait kebakaran hutan dan lahan (karhutla) di Kalimantan. Aplikasi ini terdiri dari 6 halaman yang diakses melalui sidebar navigasi.

### Stack Teknologi

| Komponen | Library / Versi |
|----------|-----------------|
| Framework UI | Streamlit (`streamlit`) |
| Data manipulation | Pandas (`pandas`) |
| Visualisasi | Plotly Express & Graph Objects (`plotly`) |
| WordCloud | `wordcloud` + `matplotlib` |
| Excel support | `openpyxl` |
| Machine Learning | `scikit-learn` (untuk LDA topic modelling di masa depan) |

### Cara Menjalankan Aplikasi

```bash
# 1. Buat virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan membuka di `http://localhost:8501`.

---

## 2. Project Architecture

### Struktur Folder (Root)

```
karhutla-threads-dashboard/
├── app.py                      # Entry point: konfigurasi halaman, CSS, navigasi sidebar
├── README.md
├── requirements.txt
├── .gitignore
├── DEVELOPMENT_GUIDE.md        # File ini
│
├── pages/                      # 6 halaman aplikasi (urutan navigasi)
│   ├── 1_Overview.py
│   ├── 2_EDA.py
│   ├── 3_Cooccurrence.py
│   ├── 4_Topic_Analysis.py
│   ├── 5_Comment_Explorer.py
│   └── 6_Insights_Conclusion.py
│
├── src/                        # Modul sumber daya (logic, config, visualization)
│   ├── __init__.py
│   ├── config.py               # Design system tunggal: path, warna, font, navigasi, mapping kolom
│   ├── data_loader.py          # Pemuatan dataset (cache)
│   ├── preprocessing.py        # Fungsi ringkasan data dasar
│   ├── eda.py                  # Stub fungsi analisis EDA (Tahap 4)
│   ├── cooccurrence.py         # Stub fungsi co-occurrence (Tahap 4)
│   ├── topic_modeling.py       # Stub fungsi topic modelling (Tahap 4)
│   ├── comment_explorer.py     # Stub fungsi comment explorer (Tahap 4)
│   ├── visualization.py        # Komponen render reusable (KPI, chart, card, banner, dll.)
│   └── utils.py                # Utility umum (CSS loader, format angka, file exists)
│
├── assets/
│   └── style.css               # Global CSS design system
│
├── data/
│   ├── raw/comments_raw.csv           # Data mentah (tidak diubah)
│   ├── processed/comments_clean.csv   # Hasil preprocessing (ditambahkan kolom text_clean)
│   ├── processed/comments_tokenized.csv
│   └── model_output/                  # Hasil pemodelan (kosong, hanya .gitkeep)
│
├── notebooks/                  # Jupyter notebook eksplorasi (kosong)
└── .streamlit/                 # Konfigurasi Streamlit (kosong)
```

### Alur Data (Data Flow)

```
data/raw/comments_raw.csv
    ↓ (preprocessing dilakukan di notebooks/, belum tersedia)
```
---

## 3. Global Configuration

File `src/config.py` adalah **satu-satunya sumber kebenaran (single source of truth)** untuk design system dan path. Semua perubahan di sini akan berlaku ke seluruh halaman.

### Path dan Direktori

| Variabel | Nilai | Keterangan |
|----------|-------|------------|
| `BASE_DIR` | `Path(__file__).resolve().parent.parent` | Root project |
| `ASSETS_DIR` | `BASE_DIR / "assets"` | Folder aset statis |
| `CSS_PATH` | `ASSETS_DIR / "style.css"` | Path file CSS global |
| `DATA_RAW_DIR` | `BASE_DIR / "data" / "raw"` | Folder data mentah |
| `DATA_PROCESSED_DIR` | `BASE_DIR / "data" / "processed"` | Folder data hasil preprocessing |
| `MODEL_OUTPUT_DIR` | `BASE_DIR / "data" / "model_output"` | Folder output model |
| `RAW_DATA_FILE` | `"comments_raw.csv"` | Nama file data mentah |
| `PROCESSED_DATA_FILE` | `"comments_clean.csv"` | Nama file data hasil preprocessing |
| `FOREST_IMAGE` | `ASSETS_DIR / "forest.png"` | Gambar ilustrasi (opsional, mungkin belum ada) |

### Identitas Aplikasi

| Variabel | Nilai | Keterangan |
|----------|-------|------------|
| `APP_NAME` | `"Dashboard Karhutla"` | Judul tab browser |
| `APP_DESCRIPTION` | `"Dashboard interaktif analisis komentar media sosial terkait kebakaran hutan dan lahan (karhutla)."` | Deskripsi aplikasi |
| `APP_ICON` | `"🔥"` | Icon tab browser |
| `SIDEBAR_TITLE` | `"DASHBOARD KARHUTLA"` | Judul di sidebar kiri |
| `PROJECT_TITLE` | `"DASHBOARD ANALISIS KOMENTAR THREADS MENGENAI KARHUTLA"` | Judul besar halaman Overview |
| `BACKGROUND_TEXT` | *(teks panjang)* | Teks latar belakang (banner kiri) |
| `OBJECTIVE_TEXT` | *(teks panjang)* | Teks tujuan (banner kanan) |

### Identitas Kelompok (Sidebar)

```python
GROUP_IDENTITY = {
    "course": "STA1381 - Pengantar Sains Data",
    "lecturer": "Septian Rahardiantoro S.Stat., M.Si., Ph.D.",
    "members": [
        "Muhammad Ayyash S.| M0401241001",
        "Daffa Lukman W. A. J. | M0401241008",
        "Shabrina Nur Izzati | M0401241011",
        "Najwa Salsabila M.N | M0401241016",
        "Uma Keisha Abriana  | M0401241022",
        "Naurah Aathirah Farid | M0401241037"
    ],
}
```

### Mapping Kolom Dataset (`COLUMNS`)

| Kunci | Nilai | Kolom Asli di CSV |
|-------|-------|-------------------|
| `"id"` | `"comment_id"` | ID komentar |
| `"user"` | `"user_id"` | ID pengguna |
| `"date"` | `"date"` | Tanggal komentar |
| `"text"` | `"comment_text"` | Isi teks komentar |
| `"likes"` | `"likes"` | Jumlah likes |
| `"shares"` | `"shares"` | Jumlah shares |
| `"replies"` | `"replies"` | Jumlah replies |
| `"text_clean"` | `"text_clean"` | Teks hasil preprocessing (hanya di `comments_clean.csv`) |

**Catatan:** `data/raw/comments_raw.csv` memiliki 7 kolom (tanpa `text_clean`). `data/processed/comments_clean.csv` memiliki 8 kolom (dengan `text_clean`).

### Langkah Alur Analisis (`WORKFLOW_STEPS`)

```python
WORKFLOW_STEPS = [
    ("Scraping Data Threads", "⬇️", "dark"),
    ("Cleaning & Case Folding", "🧹", "red"),
    ("Stopword Removal", "🚫", "orange"),
    ("Stemming", "🌱", "dark"),
    ("Tokenisasi", "✂️", "red"),
    ("Eksplorasi", "🔍", "orange"),
    ("Co-occurrence & Korelasi", "🕸️", "dark"),
    ("LDA Topic Modelling", "💡", "red"),
]
```

Setiap tuple berisi: `(label, ikon, variant)`. Variant digunakan untuk warna latar kartu alur (`flow-dark`, `flow-red`, `flow-orange`).

### Navigasi Halaman (`PAGES`)

```python
PAGES = [
    {"path": "pages/1_Overview.py", "label": "OVERVIEW", "icon": ":material/bookmark:"},
    {"path": "pages/2_EDA.py", "label": "EDA", "icon": ":material/bar_chart:"},
    {"path": "pages/3_Cooccurrence.py", "label": "CO-OCCURANCE ANALYSIS", "icon": ":material/hub:"},
    {"path": "pages/4_Topic_Analysis.py", "label": "MODELLING", "icon": ":material/lightbulb:"},
    {"path": "pages/5_Comment_Explorer.py", "label": "COMMENT EXPLORER", "icon": ":material/search:"},
    {"path": "pages/6_Insights_Conclusion.py", "label": "INSIGHT & KESIMPULAN", "icon": ":material/error:"},
]
```

### Design System (Warna, Font, Layout)

#### `COLORS`

| Kunci | Hex | Keterangan |
|-------|-----|------------|
| `green_dark` | `#1B4332` | Hijau tua (utama) |
| `red_orange` | `#D94A05` | Merah-oranye |
| `orange` | `#E85D10` | Oranye |
| `amber` | `#F58E0A` | Amber/kuning muda |
| `cream` | `#F5F0E6` | Krem (background utama) |
| `cream_light` | `#FDF9EE` | Krem sangat terang |
| `text_dark` | `#1B4332` | Teks gelap |
| `text_light` | `#FFFFFF` | Teks terang |
| `muted` | `#8A8F86` | Abu-abu netral |
| `gold` | `#C9963F` | Emas |

#### `VARIANT_COLORS` (untuk KPI card)

| Variant | Warna Latar |
|---------|-------------|
| `"dark"` | `#1B4332` (green_dark) |
| `"red"` | `#D94A05` (red_orange) |
| `"orange"` | `#F58E0A` (amber) |

#### `CHART_COLORWAY` (urutan warna kategori untuk chart)

```python
CHART_COLORWAY = [
    COLORS["green_dark"],   # #1B4332
    COLORS["orange"],       # #E85D10
    COLORS["amber"],        # #F58E0A
    COLORS["gold"],         # #C9963F
```
---

## 4. Global Styling System

File `assets/style.css` berisi semua CSS global yang diimpor oleh `src/utils.load_css()` dan diterapkan ke seluruh aplikasi melalui `app.py`.

### Cara Memuat CSS

Di `app.py`:
```python
from src.utils import load_css
load_css()  # Memuat config.CSS_PATH (assets/style.css)
```

Di dalam file CSS, font Montserrat diimpor melalui `@import url(...)` di dalam tag `<style>` yang di-generate oleh `load_css()`.

### CSS Variables (`:root`)

```css
:root {
  --green: #1B4332;
  --red: #D94A05;
  --orange: #E85D10;
  --amber: #F58E0A;
  --cream: #F5F0E6;
  --cream-light: #FDF9EE;
  --muted: #8A8F86;
  --radius: 8px;
  --shadow: 0 6px 14px rgba(27, 67, 50, 0.18);
}
```

Variabel ini dapat digunakan di seluruh aplikasi. Untuk menambahkan warna baru, tambahkan di `:root` dan juga di `src/config.py` agar sinkron.

### Class CSS yang Tersedia

| Class | Elemen | Deskripsi |
|-------|--------|-----------|
| `.page-title` | `<h1>` | Judul halaman besar (hijau, 2.6rem, uppercase) |
| `.page-title.accent` | `<h1>` | Judul versi aksen (oranye, 3.4rem, digunakan Overview) |
| `.section-header` | `<div>` | Kontainer judul section + deskripsi |
| `.section-header h3` | `<h3>` | Judul section (hijau, bold) |
| `.section-header p` | `<p>` | Deskripsi section (hijau, opacity 0.75) |
| `.info-card` | `<div>` | Kartu teks dasar (radius 8px, shadow) |
| `.info-light` | `<div>` | Kartu background krem terang |
| `.info-dark` | `<div>` | Kartu background hijau tua |
| `.info-card.placeholder` | `<div>` | Kartu placeholder (border dashed) |
| `.banner` | `<div>` | Banner hijau dengan 2 kartu putih di dalam |
| `.kpi-card` | `<div>` | Kartu KPI |
| `.kpi-card.kpi-dark` | `<div>` | KPI background hijau tua |
| `.kpi-card.kpi-red` | `<div>` | KPI background merah-oranye |
| `.kpi-card.kpi-orange` | `<div>` | KPI background amber |
| `.kpi-card.kpi-compact` | `<div>` | KPI versi kecil (min-height 90px) |
| `.kpi-value` | `<div>` | Nilai besar KPI (putih, bold) |
| `.kpi-title` | `<div>` | Judul KPI (putih) |
| `.kpi-delta` | `<div>` | Delta/ubah KPI (kecil, opacity 0.9) |
| `.pill-label` | `<div>` | Label pill berwarna |
| `.pill-dark` / `.pill-red` / `.pill-orange` | `<div>` | Variasi warna pill |
| `.badge` | `<span>` | Badge kecil (untuk tabel) |
| `.badge-red` / `.badge-green` / `.badge-amber` / `.badge-dark` | `<span>` | Variasi warna badge |
| `.notice` | `<div>` | Pesan informasi/peringatan |
| `.notice-info` / `.notice-warning` | `<div>` | Variasi warna notice |
| `.flow-panel` | `<div>` | Panel alur proses (background hijau) |
| `.flow-step` | `<div>` | Satu langkah dalam alur proses |

---

## 5. Page-by-Page Editing Guide

Setiap halaman di `pages/` adalah file Python mandiri yang dieksekusi oleh `st.navigation()`. Setiap halaman memiliki fungsi `render()` yang dipanggil di akhir file.

Pola umum setiap halaman:
```python
import streamlit as st
from src import config
from src.visualization import render_page_title, render_section_header, render_kpi

def render():
    render_page_title("JUDUL")
    # ... isi halaman ...
    # ... KPI, chart, tabel ...

render()  # Dipanggil di akhir file
```

### 5.1 Halaman 1 — Overview (`pages/1_Overview.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman pembuka yang menampilkan identitas proyek, latar belakang, tujuan, 4 KPI utama, dan alur analisis 8 langkah.
- **File Python:** `pages/1_Overview.py`
- **Fungsi utama:** `render()`
- **Helper tambahan:** `_format_periode(lo, hi)` — memformat rentang tanggal ke bahasa Indonesia.
- **Komponen yang digunakan:** `render_page_title`, `render_kpi`, `render_banner`, `render_section_header`, `render_process_flow`, `render_data_notice` dari `src.visualization`; `load_raw_data`, `load_processed_data` dari `src.data_loader`; `count_rows`, `count_unique`, `get_date_range` dari `src.preprocessing`.

#### B. Struktur Halaman dari Atas ke Bawah

| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Page Header / Title | `render_page_title(config.PROJECT_TITLE, accent=True)` | Judul besar berwarna oranye (accent) |
| 2 | Load Data | `load_raw_data()`, `load_processed_data()` | Memuat data mentah dan hasil preprocessing |
| 3 | Data Notice (jika data None) | `render_data_notice(..., level="warning")` | Ditampilkan jika file CSV tidak ditemukan |
| 4 | KPI Baris 1 | `render_kpi("Total Komentar Sebelum Pre-processing", n_raw, variant="dark")` | Total baris data mentah |
| 5 | KPI Baris 2 | `render_kpi("Total Komentar Setelah Pre-processing", n_proc, variant="red")` | Total baris data bersih |
| 6 | KPI Baris 3 | `render_kpi("Jumlah Pengguna Unik", n_user, variant="orange")` | Jumlah user_id unik |
| 7 | KPI Baris 4 | `render_kpi("Periode Pengambilan Data", "13-08-2026...", variant="dark")` | Rentang tanggal (teks statis, belum pakai `_format_periode`) |
| 8 | Banner Latar Belakang & Tujuan | `render_banner(("LATAR BELAKANG", config.BACKGROUND_TEXT), ("TUJUAN", config.OBJECTIVE_TEXT))` | Banner hijau dengan 2 kartu |
| 9 | Section Header | `render_section_header("ALUR MANAJEMEN DAN ANALISIS DATA")` | Judul section alur |
| 10 | Process Flow | `render_process_flow(config.WORKFLOW_STEPS)` | 8 kartu langkah analisis |

#### C. Panduan Editing Chart dan Visualisasi

Halaman Overview **tidak memiliki chart visualisasi** (hanya KPI card dan process flow HTML). Untuk menambahkan chart:

1. Impor fungsi chart dari `src.visualization`, mis. `render_bar_chart`.
2. Siapkan DataFrame.
3. Panggil fungsi chart di dalam `render()`.

Contoh menambahkan bar chart sederhana di bawah KPI:
```python
from src.visualization import render_bar_chart
import pandas as pd

df_summary = pd.DataFrame({
    "kategori": ["Komentar", "Pengguna", "Tanggal"],
    "jumlah": [n_raw, n_user, 1]
})
render_bar_chart(df_summary, x="kategori", y="jumlah", title="Ringkasan Data", horizontal=False)
```

#### D. Panduan Editing KPI

Fungsi `render_kpi` memiliki parameter berikut (lihat `src/visualization.py` baris 75-120):

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `title` | — | Judul KPI |
| `value` | — | Nilai (angka atau string) |
| `delta` | None | Teks delta kecil di bawah nilai |
| `variant` | `"dark"` | `"dark"`, `"red"`, `"orange"` (menentukan warna latar) |
| `compact` | `False` | Jika `True`, ukuran lebih kecil (min-height 90px, value 2rem) |
| `width` | None | CSS width, mis. `"100%"` |
| `height` | None | CSS height, mis. `"130px"` |
| `value_size` | `"3.6rem"` | Ukuran font nilai |
| `title_size` | `"1rem"` | Ukuran font judul |
| `title_line_height` | `"1.2"` | Line height judul |
| `title_margin` | `"4px"` | Margin atas judul |
| `padding` | `"22px 12px"` | Padding dalam kartu |

Contoh mengubah KPI ke variant merah dan ukuran kecil:
```python
render_kpi(
    "Total Komentar",
```

### 5.2 Halaman 2 — EDA (`pages/2_EDA.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman Exploratory Data Analysis yang menampilkan 3 KPI interaksi (likes, shares, replies) dan 4 visualisasi (WordCloud, histogram, line chart, heatmap).
- **File Python:** `pages/2_EDA.py`
- **Fungsi utama:** `render()`
- **Komponen yang digunakan:** `render_page_title`, `render_section_header`, `render_kpi`, `render_pill_label`, `render_histogram`, `render_line_chart`, `render_heatmap`, `render_wordcloud`, `render_data_notice`, `render_placeholder_card` dari `src.visualization`; `load_processed_data` dari `src.data_loader`.

#### B. Struktur Halaman dari Atas ke Bawah

| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Page Title | `render_page_title("EXPLORATORY DATA ANALYSIS")` | Judul halaman |
| 2 | Load Data | `load_processed_data()` | Memuat `comments_clean.csv` |
| 3 | Data Notice (jika None) | `render_data_notice(..., level="warning")` | Jika file tidak ditemukan |
| 4 | KPI Baris | 3 kolom: `render_kpi("Rata-rata Likes", ...)`, `"Rata-rata Shares"`, `"Rata-rata Replies"` | Menggunakan `df[...].mean()` |

#### C. Panduan Editing Chart dan Visualisasi

Chart yang tersedia di halaman ini dan fungsi pembentuknya di `src/visualization.py`:

##### 1. WordCloud (`render_wordcloud`)

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `data` | — | DataFrame |
| `text_col` | — | Nama kolom teks (mis. `"comment_text"`) |
| `title` | None | Judul chart |
| `height` | None | Tinggi figure |
| `key` | None | Streamlit key |

Library: `wordcloud` + `matplotlib`. Tidak menggunakan Plotly.

**Cara mengganti:**
```python
render_wordcloud(df, "comment_text", title="WordCloud Komentar")
```
Untuk mengubah jumlah kata maksimal, ubah di dalam fungsi `render_wordcloud` di `src/visualization.py` baris 289-296 (parameter `max_words=100`, `colormap="autumn"`, `background_color`).

**Catatan:** Parameter `key` diterima oleh fungsi tetapi **tidak** dilewatkan ke `st.pyplot` (karena `st.pyplot` tidak mendukung `key`). Jika Anda ingin menambahkan `key`, edit `src/visualization.py` baris 304.

##### 2. Histogram (`render_histogram`)

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `data` | — | DataFrame |
| `x` | — | Nama kolom numerik |
| `title` | None | Judul |
| `nbins` | None | Banyak bin |

##### 3. Line Chart (`render_line_chart`)

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `data` | — | DataFrame |
| `x` | — | Nama kolom sumbu X |
| `y` | — | Nama kolom sumbu Y |
| `title` | None | Judul |
| `color` | None | Kolom untuk pewarnaan garis |
| `markers` | `True` | Tampilkan titik pada garis |
| `height` | None | Tinggi chart |
| `key` | None | Streamlit key |

Library: Plotly Express (`px.line`).

**Contoh penggunaan:**
```python
harian = df.groupby("_tanggal").size().reset_index(name="jumlah")
harian = harian.rename(columns={"_tanggal": "tanggal"})
render_line_chart(harian, x="tanggal", y="jumlah", title="Tren jumlah komentar per hari")
```

**Cara mengubah grid:**
- `fig.update_xaxes(showgrid=False)` — baris 229 di `src/visualization.py`
- `fig.update_yaxes(gridcolor="rgba(27,67,50,0.1)")` — baris 230

##### 4. Heatmap (`render_heatmap`)

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `data` | — | DataFrame long-format (kolom x, y, z) |
| `x` | — | Nama kolom sumbu X |
| `y` | — | Nama kolom sumbu Y |
| `z` | — | Nama kolom nilai |
| `title` | None | Judul |
| `height` | None | Tinggi chart |
| `key` | None | Streamlit key |

Library: Plotly Graph Objects (`go.Heatmap`).

**Contoh penggunaan di halaman:**
```python
aktivitas = (
    df.groupby(["_hari", "_jam"])
    .size()
    .reset_index(name="jumlah")
    .rename(columns={"_hari": "hari", "_jam": "jam", "jumlah": "jumlah"})
)
render_heatmap(aktivitas, x="jam", y="hari", z="jumlah", title="Heatmap aktivitas hari x jam")
```

**Catatan bug:** Di `src/visualization.py` baris 268-269, `_show()` dipanggil **dua kali** untuk heatmap. Ini akan menghasilkan chart duplikat. Perbaikan yang direkomendasikan: hapus satu baris `_show(...)`.

##### 5. Cara Menambahkan Chart Baru

Di halaman `pages/2_EDA.py`, impor fungsi chart yang diinginkan dan panggil di dalam `render()`:

```python
from src.visualization import render_bar_chart, render_pie_chart

render_section_header("Top 10 Pengguna Paling Aktif")
```

### 5.3 Halaman 3 — Co-occurrence Analysis (`pages/3_Cooccurrence.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman kerangka (placeholder) untuk analisis co-occurrence kata (kemunculan bersama kata dalam satu komentar). Siap untuk integrasi di Tahap 4.
- **File Python:** `pages/3_Cooccurrence.py`
- **Fungsi utama:** `render()`
- **Status:** ⚠️ Placeholder — semua visualisasi adalah `render_placeholder_card`, tidak ada data aktual.
- **Modul target untuk integrasi:** `src/cooccurrence.py` (saat ini berisi stub).

#### B. Struktur Halaman dari Atas ke Bawah

| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Page Title | `render_page_title("CO- OCCURRENCE ANALYSIS")` | Judul halaman |
| 2 | Filter Minimal | `st.number_input("Minimal kata muncul bersama", ...)` + `st.button("apply")` | Simpan ke `st.session_state["co_min"]` |
| 3 | Divider | `st.divider()` | Pemisah |
| 4 | Section: Co-occurrence Network | `render_section_header("Co-occurrence Network")` + `render_placeholder_card(...)` | Placeholder jaringan kata |
| 5 | Divider | `st.divider()` | Pemisah |
| 6 | Kolom Kiri: Top 10 Pasangan Kata | `render_section_header("Top 10 Pasangan Kata")` + `render_placeholder_card(...)` | Placeholder bar chart horizontal |
| 7 | Kolom Kanan: Filter Kata Target | `st.text_input("filter", ...)` + `st.button("apply")` | Placeholder |
| 8 | Kolom Kanan: Network Kata Target | `render_section_header("Network Kata Target")` + `render_placeholder_card(...)` | Placeholder sub-jaringan |
| 9 | Data Notice | `render_data_notice(..., level="info")` | Catatan bahwa semua area adalah placeholder |

#### C. Panduan Editing Filter

Filter saat ini:
```python
min_cooccur = st.number_input(
    "Minimal kata muncul bersama", min_value=1, value=2, step=1, key="co_min"
)
apply_filter = st.button("apply", key="co_apply", use_container_width=True)
if apply_filter:
    st.session_state["co_min"] = min_cooccur
    st.success(f"Filter diterapkan: minimal {min_cooccur} kemunculan bersama.")
```

**Cara mengubah:**
- Ubah `min_value`, `value`, `step` di `st.number_input`.
- Ubah label tombol di `st.button`.
- Simpan nilai lain ke `st.session_state` untuk digunakan di seluruh halaman.

#### D. Cara Menghubungkan dengan `src/cooccurrence.py`

Setelah `src/cooccurrence.py` diimplementasikan, integrasi di halaman ini
terlihat seperti berikut:

```python
from src.data_loader import load_processed_data
from src.cooccurrence import tokenize_texts, calculate_cooccurrence, get_top_pairs
from src import config
from src.visualization import render_bar_chart, render_heatmap, render_placeholder_card, render_data_notice

df = load_processed_data()
if df is None:
    render_data_notice("Dataset belum tersedia.", level="warning")
    return

text_col = config.COLUMNS["text_clean"]
texts = df[text_col].dropna().astype(str).tolist()

min_cooccur = st.session_state.get("co_min", 2)
tokens = tokenize_texts(texts)
co_df = calculate_cooccurrence(tokens, min_cooccur=min_cooccur)

# Heatmap jaringan kata
if co_df is not None and len(co_df) > 0:
    heat_df = co_df[["kata_a", "kata_b", "jumlah"]].copy()
    render_heatmap(heat_df, x="kata_a", y="kata_b", z="jumlah",
                   title="Heatmap Co-occurrence Kata")
else:
    render_placeholder_card("Jaringan Kata",
                            "Tidak ada pasangan kata yang memenuhi filter.")

# Top 10 pasangan kata (bar chart horizontal)
if co_df is not None and len(co_df) > 0:
    top_pairs = get_top_pairs(co_df, top_n=10)
    if top_pairs is not None and len(top_pairs) > 0:
        render_bar_chart(top_pairs, x="jumlah", y="kata_a",
                         title="Top 10 Pasangan Kata", horizontal=True)

# Filter kata target
kata_target = st.session_state.get("co_target", "").strip()
if kata_target and co_df is not None:
    target_pairs = get_top_pairs(co_df, top_n=10, keyword=kata_target)
    if target_pairs is not None and len(target_pairs) > 0:
        render_bar_chart(target_pairs, x="jumlah", y="kata_a",
                         title=f"Network Kata: '{kata_target}'", horizontal=True)
```

### 5.4 Halaman 4 — Topic Analysis / Modelling (`pages/4_Topic_Analysis.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman kerangka (placeholder) untuk topic modelling dengan LDA. Dirancang untuk menampilkan proporsi topik, skor koherens, perbandingan topik A/B, dan tren komentar per hari per topik.
- **File Python:** `pages/4_Topic_Analysis.py`
- **Fungsi utama:** `render()`
- **Status:** ⚠️ Placeholder — semua visualisasi adalah `render_placeholder_card`, tidak ada pemodelan.
- **Modul target untuk integrasi:** `src/topic_modeling.py` (saat ini berisi stub).

#### B. Struktur Halaman dari Atas ke Bawah

| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Section: Proporsi + Koherens | `render_section_header("Proporsi Komentar Per Topik")` + `render_placeholder_card(...)` | Placeholder donut chart |
| 2 | Section: Skor Koherens | `render_section_header("Skor Koherens")` + `render_placeholder_card(...)` | Placeholder line chart |
| 3 | Divider | `st.divider()` | Pemisah |
| 4 | Section: Perbandingan Topik | `render_section_header("Perbandingan Topik")` | |
| 5 | Pemilih Topik A/B | `st.selectbox("Topik A", ...)` + `st.selectbox("Topik B", ...)` + `st.button("Apply")` | Opsi hardcoded: Topik 1-4 |
| 6 | Divider | `st.divider()` | Pemisah |
| 7 | KPI Perbandingan | 4 kolom KPI: Jumlah Komentar, Rata-rata Likes, Replies, Shares | Semua pakai `config.EMPTY_VALUE` |
| 8 | Divider | `st.divider()` | Pemisah |
| 9 | Section: Tren per Hari | `render_section_header("Tren Jumlah Komentar per hari")` + `render_placeholder_card(...)` | Placeholder line chart |
| 10 | Kontrol Model | `st.slider("λ", 0.0, 1.0, 0.5, disabled=True)` + `render_kpi("top x kata topik A/B", ...)` | Placeholder |
| 11 | Data Notice | `render_data_notice(..., level="info")` | Catatan bahwa halaman adalah kerangka |

#### C. Panduan Editing Pemilih Topik A/B

```python
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    st.selectbox(
        "Topik A",
        options=["Topik 1", "Topik 2", "Topik 3", "Topik 4"],
        index=0,
        key="tp_topik_a"
    )
with c2:
    st.selectbox(
        "Topik B",
        options=["Topik 1", "Topik 2", "Topik 3", "Topik 4"],
        index=1,
        key="tp_topik_b"
    )
with c3:
    st.write("")
    st.button("Apply", key="tp_apply", use_container_width=True)
```

**Cara mengubah jumlah topik:** Ubah daftar `options` di kedua `st.selectbox`. Nilai ini seharusnya disesuaikan dengan jumlah topik sebenarnya dari hasil LDA.

#### D. Cara Menghubungkan dengan `src/topic_modeling.py`

Setelah `src/topic_modeling.py` diimplementasikan, integrasi di halaman ini
terlihat seperti berikut:

```python
from src.data_loader import load_processed_data
from src.topic_modeling import (
    preprocess_texts, run_lda, coherence_scores,
    topic_proportion, top_words_per_topic,
)
from src import config
from src.visualization import (
    render_donut_chart, render_line_chart, render_bar_chart,
    render_placeholder_card, render_data_notice,
)

df = load_processed_data()
if df is None:
    render_data_notice("Dataset belum tersedia.", level="warning")
    return

text_col = config.COLUMNS["text_clean"]
texts = df[text_col].dropna().astype(str).tolist()

# Preprocessing + LDA
tokens = preprocess_texts(texts)
n_topics = 4
model, df_topik = run_lda(tokens, n_topics=n_topics)

# Donut: proporsi komentar per topik
if model is not None:
    proporsi = topic_proportion(model, df)
    if proporsi is not None and len(proporsi) > 0:
        render_donut_chart(proporsi, names="topik", values="proporsi",
                           title="Proporsi Komentar Per Topik")

# Line: skor koherens untuk berbagai n_topik
if model is not None:
    models_range = []
    for k in range(2, 9):
        m_k, _ = run_lda(tokens, n_topics=k)
        if m_k is not None:
            models_range.append((k, m_k))
    koherens_df = coherence_scores(models_range)
    if koherens_df is not None and len(koherens_df) > 0:
        render_line_chart(koherens_df, x="n_topik", y="koherens",
                          title="Skor Koherens per Jumlah Topik", markers=True)

# Bar: top kata per topik
if model is not None:
    top_words = top_words_per_topic(model, n=10)
    if top_words is not None and len(top_words) > 0:
        render_bar_chart(top_words, x="bobot", y="kata",
                         title="Top Kata Per Topik", horizontal=True)
```

### 5.5 Halaman 5 — Comment Explorer (`pages/5_Comment_Explorer.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman kerangka (placeholder) untuk mengeksplorasi komentar dengan filter tanggal, topik, dan pencarian teks, serta menampilkan tabel komentar dengan pagination.
- **File Python:** `pages/5_Comment_Explorer.py`
- **Fungsi utama:** `render()`
- **Status:** ⚠️ Placeholder — semua analisis dan tabel adalah placeholder.
- **Modul target untuk integrasi:** `src/comment_explorer.py` (saat ini berisi stub).

#### B. Struktur Halaman dari Atas ke Bawah

| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Page Title | `render_page_title("COMMENT EXPLORER")` | Judul halaman |
| 2 | Baris Filter | 5 kolom: `st.date_input("Dari tanggal")`, `st.date_input("Sampai tanggal")`, `st.selectbox("Topik")`, `st.text_input("Cari Komentar")`, `st.button("apply")` | Semua filter menyimpan ke `st.session_state` |
| 3 | Divider | `st.divider()` | Pemisah |
| 4 | Kolom Kiri: Ringkasan | `render_section_header("Ringkasan")` + 3x `render_info_card(...)` | Semua pakai `config.EMPTY_VALUE` |
| 5 | Kolom Kanan: Daftar Komentar | `render_section_header("Daftar Komentar")` + `render_placeholder_card(...)` | Placeholder tabel |
| 6 | Badge Example | `render_data_notice(..., level="info")` | Penjelasan tentang `render_badge` |
| 7 | Data Notice | `render_data_notice(..., level="info")` | Catatan bahwa halaman adalah kerangka |

#### C. Panduan Editing Filter

```python
c1, c2, c3, c4, c5 = st.columns([1.6, 1.6, 1.6, 2.2, 0.9])
with c1:
    st.date_input("Dari tanggal", key="ce_from", value=None)
with c2:
    st.date_input("Sampai tanggal", key="ce_to", value=None)
with c3:
    st.selectbox(
        "Topik",
        options=["Topik 1", "Topik 2", "Topik 3", "Topik 4"],
        index=None,
        placeholder="Pilih topik...",
        key="ce_topic",
    )
with c4:
    st.text_input("Cari Komentar", placeholder="cari kata kunci...", key="ce_query")
with c5:
    st.write("")
    st.button("apply", key="ce_apply", use_container_width=True)
```

**Cara menambahkan filter baru:** Tambahkan kolom baru dengan `st.columns()` atau tambahkan widget di dalam kolom yang ada.

#### D. Cara Menghubungkan dengan `src/comment_explorer.py`

Setelah diimplementasikan:
```python
from src.comment_explorer import filter_comments, summary_stats, paginate

df_view = filter_comments(df, date_range=(ce_from, ce_to), topic=ce_topic, query=ce_query)
stats = summary_stats(df_view)
df_page, total_pages = paginate(df_view, page=1, page_size=10)

# Tampilkan ringkasan
render_info_card("Total komentar", stats["total"])
render_info_card("Topik terbanyak", stats["topik_terbanyak"])
render_info_card("Rata-rata likes", stats["rata_rata_likes"])

# Tampilkan tabel
st.dataframe(df_page)
```

### 5.6 Halaman 6 — Insight & Kesimpulan (`pages/6_Insights_Conclusion.py`)

#### A. Gambaran Umum

- **Tujuan:** Halaman untuk rangkuman insight dan kesimpulan dari seluruh analisis dashboard. Saat ini semua konten adalah placeholder.
- **File Python:** `pages/6_Insights_Conclusion.py`
- **Fungsi utama:** `render()`
- **Status:** ⚠️ Placeholder — tidak ada hasil analisis atau kesimpulan yang dipersiapkan.

#### B. Struktur Halaman dari Atas ke Bawah


---

## 6. Topic Modelling Module

### Audit `src/topic_modeling.py`

File ini berisi **semua fungsi sebagai stub (kerangka sintaks tanpa implementasi asli)**. Tidak ada pemodelan, hasil topik, atau angka analisis yang dijalankan.

#### Fungsi yang Tersedia (Semua Stub)

| Fungsi | Signature | Return (Saatu Ini) | Keterangan |
|--------|-----------|-------------------|------------|
| `preprocess_texts` | `(texts: List[str]) -> List[List[str]]` | `[]` | Stub: cleansing hingga tokenisasi |
| `run_lda` | `(tokens_per_doc: List[List[str]], n_topics: int) -> Tuple[Optional[object], Optional[pd.DataFrame]]` | `(None, None)` | Stub: pelatihan model LDA |
| `coherence_scores` | `(models_range) -> Optional[pd.DataFrame]` | `None` | Stub: skor koherens untuk berbagai n_topik |
| `topic_proportion` | `(model, df: pd.DataFrame) -> Optional[pd.DataFrame]` | `None` | Stub: proporsi komentar per topik |
| `top_words_per_topic` | `(model, n: int = 10) -> Optional[pd.DataFrame]` | `None` | Stub: n kata teratas per topik |

#### Format Input dan Output yang Direncanakan

| Fungsi | Input | Output yang Diharapkan |
|--------|-------|----------------------|
| `preprocess_texts` | `List[str]` (daftar teks komentar) | `List[List[str]]` (daftar token per dokumen) |
| `run_lda` | `List[List[str]]` (tokens), `int` (n_topics) | `model` (object LDA), `pd.DataFrame` (topik per dokumen) |
| `coherence_scores` | `range` atau `list` of model LDA | `pd.DataFrame` dengan kolom `['n_topik', 'koherens']` |
| `topic_proportion` | `model`, `pd.DataFrame` | `pd.DataFrame` dengan kolom `['topik', 'proporsi']` |
| `top_words_per_topic` | `model`, `int` n | `pd.DataFrame` dengan kolom `['topik', 'kata', 'bobot']` |

#### Alur Preprocessing hingga Topic Modelling

```
teks komentar
    ↓ preprocess_texts()
cleaning / case folding / stopword removal / stemming / tokenisasi
    ↓ run_lda(tokens, n_topics)
vektorisasi (CountVectorizer / TfidfVectorizer) → LDA
    ↓
model LDA + topik per dokumen
    ↓ topic_proportion(model, df)
proporsi komentar per topik → donut chart
    ↓ top_words_per_topic(model, n)
kata teratas per topik → bar chart
    ↓ coherence_scores(models_range)
skor koherens → line chart
```

#### Cara Mengimplementasikan Fungsi Baru (Rekomendasi)

Contoh implementasi `run_lda` menggunakan `scikit-learn` (sudah ada di `requirements.txt`):

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd

def run_lda(tokens_per_doc: List[List[str]], n_topics: int):
    texts = [" ".join(tokens) for tokens in tokens_per_doc]
    vectorizer = CountVectorizer(max_df=0.95, min_df=2)
    X = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    topic_dist = lda.transform(X)
    topik_per_dokumen = topic_dist.argmax(axis=1)
    df_topik = pd.DataFrame({
        "topik": [f"Topik {i+1}" for i in topik_per_dokumen]
    })
```
---

## 7. Analytics Module

### Audit `src/eda.py`

File ini berisi stub fungsi analisis EDA. Semua fungsi mengembalikan `None` atau placeholder.

| Fungsi | Signature | Return | Status |
|--------|-----------|--------|--------|
| `calculate_total_comments` | `(df: Optional[pd.DataFrame]) -> Optional[int]` | `int(len(df))` atau `None` | ✅ Implementasi lengkap |
| `calculate_sentiment_distribution` | `(df: Optional[pd.DataFrame])` | `None` | ⚠️ Stub (belum ada kolom sentimen) |
| `calculate_average_metric` | `(df: Optional[pd.DataFrame], column: str) -> Optional[float]` | `float` atau `None` | ✅ Implementasi lengkap |

#### Fungsi yang Belum Dibuat di `src/eda.py`

- Analisis distribusi sentimen (positif/negatif/netral)
- Analisis kata teratas (frequency)
- Analisis tren waktu lengkap
- Analisis demografi pengguna

### Audit `src/cooccurrence.py`

| Fungsi | Signature | Return | Status |
|--------|-----------|--------|--------|
| `tokenize_texts` | `(texts: List[str]) -> List[List[str]]` | `[t.split() for t in texts]` | ⚠️ Stub (sederhana, tanpa cleaning) |
| `calculate_cooccurrence` | `(tokens_per_doc, min_cooccur=2) -> Optional[pd.DataFrame]` | `None` | ⚠️ Stub |
| `get_top_pairs` | `(cooccurrence_df, top_n=10, keyword=None) -> Optional[pd.DataFrame]` | `None` | ⚠️ Stub |

### Audit `src/comment_explorer.py`

| Fungsi | Signature | Return | Status |
|--------|-----------|--------|--------|
| `filter_comments` | `(df, date_range=None, topic=None, query=None) -> Optional[pd.DataFrame]` | `df` (tidak difilter) | ⚠️ Stub |
| `summary_stats` | `(df: Optional[pd.DataFrame]) -> dict` | `{"total": None, "topik_terbanyak": None, "rata_rata_likes": None}` | ⚠️ Stub |
| `paginate` | `(df, page=1, page_size=10) -> Tuple[Optional[pd.DataFrame], int]` | `(df, 1)` | ⚠️ Stub |

---

## 8. Other Modules

### `src/data_loader.py`

| Fungsi | Signature | Keterangan |
|--------|-----------|------------|
| `find_data_file` | `(directory, filename=None) -> Optional[Path]` | Cari file dataset di folder |
| `_read_file` | `(path_str, mtime)` (cached) | Baca CSV atau Excel dengan `@st.cache_data` |
| `load_dataset` | `(directory, filename=None) -> Optional[pd.DataFrame]` | Muat dataset, return None jika gagal |
| `load_raw_data` | `() -> Optional[pd.DataFrame]` | Muat `data/raw/comments_raw.csv` |
| `load_processed_data` | `() -> Optional[pd.DataFrame]` | Muat `data/processed/comments_clean.csv` |

**Cara menambahkan data source baru:**
```python
def load_custom_data(filename: str) -> Optional[pd.DataFrame]:
    return load_dataset(config.DATA_RAW_DIR, filename)
```

### `src/preprocessing.py`

| Fungsi | Signature | Keterangan |
|--------|-----------|------------|
| `count_rows` | `(df) -> Optional[int]` | Jumlah baris |
| `count_unique` | `(df, column) -> Optional[int]` | Jumlah nilai unik |
| `get_date_range` | `(df, column) -> Optional[tuple]` | `(min_date, max_date)` |

### `src/utils.py`

| Fungsi | Signature | Keterangan |
|--------|-----------|------------|
| `load_css` | `(css_path=None)` | Muat file CSS global |
| `format_number` | `(value)` | Format angka dengan pemisah ribuan titik (gaya Indonesia) |
| `format_percentage` | `(value, decimals=1)` | Format rasio 0-1 menjadi persen |
| `check_file_exists` | `(path)` | Cek apakah file ada |

### `src/visualization.py`

Fungsi render yang tersedia (18+ fungsi):

| Fungsi | Parameter Utama | Keterangan |
|--------|----------------|------------|
| `render_page_title` | `(title, accent=False)` | Judul halaman besar |
| `render_section_header` | `(title, description=None)` | Judul section + deskripsi |
| `render_kpi` | `(title, value, delta=None, variant="dark", compact=False, width=None, height=None, value_size="3.6rem", title_size="1rem", title_line_height="1.2", title_margin="4px", padding="22px 12px")` | KPI card |
| `render_info_card` | `(title, content, variant="light")` | Kartu teks |
| `render_banner` | `(left, right)` | Banner hijau dengan 2 kartu |
| `render_pill_label` | `(text, variant="dark")` | Label pill berwarna |
| `render_badge` | `(text, variant="red")` | Return string HTML badge |
| `render_data_notice` | `(message, level="info")` | Pesan info/warning |
| `render_placeholder_card` | `(title, message="...")` | Kartu placeholder |

---

## 9. How to Add a New Page

### Langkah-langkah

#### 1. Buat file halaman baru

Buat file `pages/7_NamaHalaman.py` dengan pola berikut:

```python
"""Halaman Nama Halaman — deskripsi singkat."""

import streamlit as st
from src import config
from src.visualization import render_page_title, render_section_header, render_kpi

def render():
    render_page_title("NAMA HALAMAN")
    
    # Isi halaman di sini
    render_section_header("Section Pertama")
    render_kpi("Contoh KPI", 123, variant="dark")

render()
```

#### 2. Daftarkan halaman pada sistem navigasi

Edit `src/config.py`, tambahkan entri baru di list `PAGES`:

```python
PAGES = [
    # ... entri existing ...
    {"path": "pages/7_NamaHalaman.py", "label": "NAMA HALAMAN", "icon": ":material/thumb_up:"},
]
```

#### 3. Hubungkan komponen

Impor fungsi `render_*` dari `src.visualization` dan panggil di dalam `render()`.

#### 4. Hubungkan data

Impor `load_processed_data` atau `load_raw_data` dari `src.data_loader`, lalu panggil di dalam `render()`:

```python
from src.data_loader import load_processed_data

df = load_processed_data()
if df is None:
    from src.visualization import render_data_notice
    render_data_notice("Data belum tersedia.", level="warning")
    return
```

#### 5. Hubungkan fungsi analytics atau modelling


---

## 10. How to Add a New Feature

### 10.1 Menambahkan Chart Baru

1. Tentukan jenis chart (bar, line, pie, donut, histogram, heatmap).
2. Impor fungsi render yang sesuai dari `src.visualization.py`.
3. Siapkan DataFrame dengan kolom yang sesuai.
4. Panggil fungsi chart di dalam `render()` halaman.

Contoh menambahkan pie chart di halaman Overview:
```python
from src.visualization import render_pie_chart
import pandas as pd

df_pie = pd.DataFrame({
    "kategori": ["Positif", "Netral", "Negatif"],
    "jumlah": [100, 200, 50]
})
render_pie_chart(df_pie, names="kategori", values="jumlah", title="Distribusi Sentimen")
```

### 10.2 Menambahkan KPI Baru

1. Di halaman yang diinginkan, tambahkan kolom baru dengan `st.columns()`.
2. Panggil `render_kpi()` dengan parameter yang diinginkan.

Contoh:
```python
col1, col2 = st.columns(2)
with col1:
    render_kpi("Total Komentar", n_raw, variant="dark")
with col2:
    render_kpi("Rata-rata Likes", round(df["likes"].mean(), 2), variant="red")
```

### 10.3 Menambahkan Filter Baru

1. Tambahkan widget Streamlit (`st.date_input`, `st.selectbox`, `st.text_input`, `st.number_input`, `st.slider`) di dalam `st.columns()`.
2. Simpan nilai ke `st.session_state` jika diperlukan di seluruh halaman.
3. Terapkan filter pada DataFrame sebelum visualisasi.

Contoh:
```python
min_likes = st.number_input("Minimal Likes", min_value=0, value=0, key="filter_min_likes")
df_filtered = df[df["likes"] >= min_likes]
```

### 10.4 Menambahkan Data Source Baru

1. Letakkan file data di `data/raw/` atau `data/processed/`.
2. Di `src/config.py`, tambahkan variabel nama file baru atau gunakan `find_data_file()`.
3. Buat fungsi pemuat di `src/data_loader.py` atau gunakan `load_dataset()` langsung.

Contoh:
```python
from src.data_loader import load_dataset
from src import config

df_custom = load_dataset(config.DATA_RAW_DIR, "file_baru.csv")
```

### 10.5 Menambahkan Fungsi Preprocessing

1. Tambahkan fungsi di `src/preprocessing.py`.
2. Impor dan panggil di halaman yang membutuhkan.

Contoh:
```python
def clean_text(text: str) -> str:
    return text.lower().strip()

# Di halaman:
df["comment_text"] = df["comment_text"].apply(clean_text)
```

### 10.6 Menambahkan Metode Modelling Baru

1. Tambahkan fungsi di `src/topic_modeling.py` (atau buat file baru di `src/`).
2. Implementasikan logika model (mis. NMF, BERTopic, dll.).
3. Kembalikan output dalam format DataFrame yang konsisten dengan fungsi existing.
4. Hubungkan ke halaman `pages/4_Topic_Analysis.py`.

### 10.7 Menambahkan Analisis Baru

1. Tambahkan fungsi di `src/eda.py` atau `src/cooccurrence.py`.
2. Pastikan fungsi menangani `df=None` dengan aman (return `None`).
3. Panggil dari halaman dan tampilkan hasil dengan `render_kpi`, `render_bar_chart`, dll.

### 10.8 Menambahkan Insight Otomatis

1. Buat fungsi yang menganalisis DataFrame dan menghasilkan teks insight.
2. Tampilkan dengan `render_info_card()` di halaman Insight atau halaman lainnya.


---

## 11. Custom Design Without Global Styling

### Masalah

Global CSS di `assets/style.css` diterapkan ke seluruh aplikasi melalui `load_css()` di `app.py`. Jika Anda ingin membuat halaman dengan desain sendiri (mis. tema biru) tanpa mengubah global design system, Anda perlu menggunakan **scoped CSS** atau **inline style**.

### 1. Cara Membuat CSS Khusus Halaman

Di dalam file halaman, tambahkan CSS dengan class unik yang hanya berlaku untuk halaman tersebut:

```python
import streamlit as st

st.markdown("""
<style>
.custom-page {
    --primary: #2563EB;
    --background: #EFF6FF;
    --text: #1E293B;
    --radius: 12px;
}
.custom-page .custom-card {
    background: var(--background);
    border: 2px solid var(--primary);
    border-radius: var(--radius);
    padding: 16px;
    color: var(--text);
}
.custom-page .custom-title {
    color: var(--primary);
    font-weight: 800;
    font-size: 1.5rem;
}
</style>
""", unsafe_allow_html=True)
```

### 2. Cara Menggunakan Class atau ID Sendiri

```python
st.markdown("""
<div class='custom-page'>
    <h1 class='custom-title'>Judul Halaman dengan Tema Biru</h1>
    <div class='custom-card'>
        Konten dengan desain independen
    </div>
</div>
""", unsafe_allow_html=True)
```

### 3. Cara Melakukan Override terhadap CSS Global

Gunakan CSS selector yang lebih spesifik atau `!important`:

```css
.custom-page .stButton > button {
    background: #2563EB !important;
    color: #fff !important;
    border-radius: 6px !important;
}
```

### 4. Cara Membuat Komponen dengan Styling Independen

Gunakan `st.markdown` dengan `unsafe_allow_html=True` dan style inline:

```python
st.markdown(
    "<div style='background:#2563EB; color:white; padding:20px; border-radius:8px;'>"
    "Komponen dengan styling sendiri</div>",
    unsafe_allow_html=True
)
```

### 5. Cara Menggunakan Warna, Font, Spacing, dan Layout Sendiri

Definisikan CSS variables di dalam class scoped:

```css
.custom-page {
    --primary: #2563EB;
    --secondary: #1D4ED8;
    --background: #EFF6FF;
    --text: #1E293B;
    --font: 'Inter', sans-serif;
}
```

### 6. Cara Mencegah CSS Halaman Lain Ikut Berubah

**Penting:** Streamlit tidak secara native mendukung CSS yang scoped hanya ke satu halaman. CSS yang di-inject melalui `st.markdown` akan berlaku ke seluruh aplikasi. Untuk mencegah dampak ke halaman lain:

1. Gunakan class nama yang unik dan spesifik (mis. `.custom-page-7-komentar`).
2. Semua elemen di dalam halaman harus dibungkus dengan class induk tersebut.
3. Tidak ada cara sempurna untuk isolasi CSS di Streamlit tanpa custom component.

Contoh pendekatan yang aman:
```python
st.markdown("""
<style>
/* Hanya elemen di dalam .custom-page-7 yang terpengaruh */
.custom-page-7 .kpi-card {
    background: #2563EB !important;
}
.custom-page-7 .page-title {
    color: #2563EB !important;
}
</style>
<div class='custom-page-7'>
    <!-- isi halaman di sini -->
</div>
""", unsafe_allow_html=True)
```

### 7. Cara Menghindari Konflik Selector CSS

- Hindari menggunakan selector global seperti `button`, `input`, `h1` tanpa class induk.
- Selalu bungkus konten custom dengan `div` yang memiliki class unik.
- Gunakan prefix nama class dengan nama halaman (mis. `.overview-custom`, `.eda-custom`).
- Jika perlu override global styling, gunakan `!important` dengan hati-hati.

### Contoh Lengkap: Halaman dengan Tema Biru

```python
import streamlit as st
from src.visualization import render_kpi

# CSS scoped untuk halaman ini saja
st.markdown("""
<style>
.blue-theme {
    --primary: #2563EB;
""")
```
---

## 12. Missing Components and Recommendations

Berikut adalah daftar komponen atau file yang seharusnya tersedia tetapi belum ada, dikelompokkan berdasarkan prioritas.

### A. Critical (Diperlukan agar alur utama berjalan)

| Nama File / Komponen | Fungsi yang Diharapkan | Alasan | Hubungan dengan File Lain | Prioritas |
|----------------------|------------------------|--------|---------------------------|-----------|
| `src/topic_modeling.py` (implementasi asli) | Fungsi `run_lda`, `preprocess_texts`, `coherence_scores`, `topic_proportion`, `top_words_per_topic` yang benar-benar bekerja | Halaman 4 (Topic Analysis) adalah placeholder sepenuhnya | `pages/4_Topic_Analysis.py`, `src/visualization.py` | Tinggi |
| `src/cooccurrence.py` (implementasi asli) | Fungsi `calculate_cooccurrence`, `get_top_pairs` yang bekerja | Halaman 3 (Co-occurrence) adalah placeholder sepenuhnya | `pages/3_Cooccurrence.py`, `src/visualization.py` | Tinggi |
| `src/comment_explorer.py` (implementasi asli) | Fungsi `filter_comments`, `summary_stats`, `paginate` yang bekerja | Halaman 5 (Comment Explorer) adalah placeholder sepenuhnya | `pages/5_Comment_Explorer.py`, `src/visualization.py` | Tinggi |
| `data/model_output/` dengan file output | Folder untuk menyimpan hasil model LDA, co-occurrence, dll. | Saat ini kosong, hanya `.gitkeep` | `src/topic_modeling.py`, `src/cooccurrence.py` | Tinggi |
| Perbaikan bug `render_heatmap` di `src/visualization.py` | Hapus pemanggilan `_show()` ganda (baris 268-269) | Heatmap akan render dua kali, menyebabkan duplikat chart | `pages/2_EDA.py` | Tinggi |

### B. Recommended (Meningkatkan kualitas analisis, visualisasi, usability)

| Nama File / Komponen | Fungsi yang Diharapkan | Alasan | Hubungan dengan File Lain | Prioritas |
|----------------------|------------------------|--------|---------------------------|-----------|
| `notebooks/01_preprocessing.ipynb` | Notebook untuk preprocessing teks (cleaning, stopword, stemming, tokenisasi) | Hasil preprocessing harus tersedia di `data/processed/comments_clean.csv` | `src/preprocessing.py`, `data/processed/` | Tinggi |
| `src/eda.py` (implementasi asli) | `calculate_sentiment_distribution`, fungsi analisis lainnya | Saat ini hanya stub | `pages/2_EDA.py` | Sedang |
| Filter interaktif di `pages/2_EDA.py` | `st.date_input`, `st.selectbox` untuk filter data EDA | Saat ini EDA menampilkan semua data tanpa filter | `src/data_loader.py` | Sedang |
| `render_bar_chart` digunakan di halaman | Fungsi `render_bar_chart` ada di `src/visualization.py` tetapi belum pernah dipakai | Chart bar sangat berguna untuk top kata, top pengguna, dll. | `src/visualization.py` | Sedang |
| `render_donut_chart` digunakan di halaman 4 | Fungsi `render_donut_chart` ada tetapi belum dipakai | Diperlukan untuk proporsi topik | `pages/4_Topic_Analysis.py` | Sedang |
| File `.streamlit/config.toml` | Konfigurasi Streamlit (theme, server, dll.) | Folder `.streamlit` ada tetapi kosong | `app.py` | Rendah |


---

## 13. Troubleshooting

### 13.1 Error ketika menjalankan Streamlit

**Gejala:** `streamlit run app.py` gagal atau muncul error di terminal.

| Penyebab | Solusi |
|----------|--------|
| Virtual environment tidak aktif | Aktifkan `.venv\Scripts\Activate.ps1` (Windows) sebelum menjalankan |
| Dependensi belum terinstal | Jalankan `pip install -r requirements.txt` |
| Port 8501 sudah digunakan | Jalankan dengan port lain: `streamlit run app.py --server.port 8502` |

### 13.2 Module Not Found

**Gejala:** `ModuleNotFoundError: No module named 'src'` atau `No module named 'plotly'`.

| Penyebab | Solusi |
|----------|--------|
| `src` tidak dikenali sebagai package | Pastikan ada file `src/__init__.py` (sudah ada, kosong) |
| Jalankan dari directory yang salah | Jalankan `streamlit run app.py` dari root project, bukan dari `src/` |
| Library belum terinstal | Jalankan `pip install -r requirements.txt` |

### 13.3 Import Error

**Gejala:** `ImportError: cannot import name 'load_css' from 'src.utils'`.

| Penyebab | Solusi |
|----------|--------|
| Nama fungsi salah | Periksa ejaan fungsi di `src/utils.py`: `load_css`, `format_number`, `format_percentage`, `check_file_exists` |
| Import path salah | Gunakan `from src.utils import load_css` (dari root), bukan `from utils import load_css` |

### 13.4 File atau Path Tidak Ditemukan

**Gejala:** `FileNotFoundError` atau halaman menampilkan `render_data_notice` dengan pesan "Dataset belum tersedia".

| Penyebab | Solusi |
|----------|--------|
| File CSV tidak ada di `data/raw/` atau `data/processed/` | Pastikan `comments_raw.csv` dan `comments_clean.csv` ada |
| Nama file salah | Periksa `config.RAW_DATA_FILE` dan `config.PROCESSED_DATA_FILE` di `src/config.py` |
| Path relatif tidak cocok | `config.BASE_DIR` menggunakan `Path(__file__).resolve().parent.parent`, harus benar jika struktur folder tidak diubah |

### 13.5 Dataframe Kosong

**Gejala:** Chart tidak muncul, KPI menampilkan `—` (EMPTY_VALUE).

| Penyebab | Solusi |
|----------|--------|
| `load_processed_data()` mengembalikan `None` | Periksa apakah `data/processed/comments_clean.csv` ada dan bisa dibaca |
| DataFrame kosong (0 baris) | Fungsi `_is_empty` di `src/visualization.py` akan memicu `_empty_notice` |
| Kolom tidak ada di DataFrame | Periksa `config.COLUMNS` di `src/config.py` dan bandingkan dengan header CSV asli |

### 13.6 Chart Tidak Muncul

**Gejala:** Area chart kosong atau tidak ada visualisasi.

| Penyebab | Solusi |
|----------|--------|
| Data input ke fungsi chart adalah `None` atau kosong | Semua fungsi chart memeriksa `_is_empty(data)` dan akan menampilkan notice |
| `render_heatmap` duplikat | Bug di `src/visualization.py` baris 268-269: `_show()` dipanggil dua kali. Hapus satu baris. |
| `render_wordcloud` dengan parameter `key` | `st.pyplot` tidak mendukung `key`. Jika melewatkan `key`, akan error. Edit `src/visualization.py` baris 304 untuk menghapus `key=key` dari `st.pyplot`. |

### 13.7 CSS Tidak Terbaca

**Gejala:** Tampilan halaman tidak sesuai dengan `assets/style.css`.

| Penyebab | Solusi |
|----------|--------|
| `load_css()` tidak dipanggil | Pastikan `app.py` memanggil `load_css()` sebelum `pg.run()` |
| File CSS tidak ada | Periksa `assets/style.css` ada dan path di `config.CSS_PATH` benar |
| Cache browser | Hard refresh (Ctrl+F5) atau buka dalam mode incognito |


---

## 14. Development Workflow

### 14.1 Setup Awal

```bash
# Clone repository (jika belum)
git clone https://github.com/shabrinanurizz/karhutla-threads-dashboard.git
cd karhutla-threads-dashboard

# Buat virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependensi
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

### 14.2 Workflow Edit Halaman

1. Buka file halaman di `pages/X_*.py`.
2. Identifikasi section yang ingin diedit berdasarkan [5. Page-by-Page Editing Guide](#5-page-by-page-editing-guide).
3. Ubah parameter fungsi `render_*` atau tambahkan fungsi baru.
4. Jika perlu mengubah warna/font global, edit `src/config.py` dan `assets/style.css`.
5. Jalankan `streamlit run app.py` dan verifikasi di browser.
6. Jika menambahkan data baru, letakkan file di `data/raw/` atau `data/processed/`.

### 14.3 Workflow Menambahkan Fitur Baru

1. Tentukan fitur apa yang ingin ditambahkan (chart, KPI, filter, modelling, dll.).
2. Jika memerlukan fungsi baru, tambahkan di modul `src/` yang sesuai.
3. Impor fungsi di halaman `pages/X_*.py`.
4. Panggil fungsi di dalam `render()`.
5. Uji dengan menjalankan aplikasi.
6. Dokumentasikan perubahan di `README.md` jika diperlukan.

### 14.4 Testing

- **Manual testing:** Jalankan `streamlit run app.py`, buka setiap halaman melalui sidebar, verifikasi tidak ada error.
- **Data testing:** Pastikan `data/raw/comments_raw.csv` dan `data/processed/comments_clean.csv` bisa dibaca oleh `load_raw_data()` dan `load_processed_data()`.
- **Chart testing:** Pastikan semua chart muncul dengan data yang benar, tidak ada area kosong yang tidak diinginkan.
- **CSS testing:** Periksa tampilan di berbagai ukuran layar (responsif).

### 14.5 Checklist Sebelum Commit

- [ ] Semua file di `pages/` dapat diimpor tanpa error.
- [ ] `streamlit run app.py` berjalan tanpa exception.
- [ ] Tidak ada fungsi stub yang dipanggil tanpa penanganan `None`.
- [ ] Semua import menggunakan path yang benar (`from src import ...`).
- [ ] Jika mengubah `src/config.py`, verifikasi semua halaman masih tampil dengan benar.
- [ ] Tidak ada file besar atau sensitif yang di-commit ke git.

---

## Catatan Penting untuk Developer

1. **Jangan mengubah struktur project tanpa alasan yang jelas.** Semua path di `src/config.py` tergantung pada struktur folder saat ini.
2. **Semua perubahan di `src/config.py` berlaku global** karena design system terpusat di sana.
3. **Fungsi stub di `src/eda.py`, `src/cooccurrence.py`, `src/topic_modeling.py`, dan `src/comment_explorer.py` belum mengembalikan data aktual.** Jangan mengandalkan nilai kembaliannya untuk produksi sebelum diimplementasikan.
4. **`render_heatmap` di `src/visualization.py` memiliki bug pemanggilan `_show()` ganda.** Perbaikan disarankan sebelum menggunakan heatmap secara luas.
5. **`render_wordcloud` tidak mendukung parameter `key` ke `st.pyplot`.** Jika Anda melewatkan `key`, akan terjadi error.
6. **Tidak ada file `app.py` atau `main.py` terpisah di luar root.** Entry point adalah `app.py` di root project.
7. **Semua halaman menggunakan pola `def render():` yang dipanggil di akhir file.** Ikuti pola ini untuk halaman baru.

---

*Dokumentasi ini dibuat berdasarkan audit menyeluruh terhadap seluruh struktur project `karhutla-threads-dashboard`. Semua nama file, fungsi, parameter, dan path telah diverifikasi langsung dari source code. Dokumentasi ini tidak berisi asumsi atau contoh generik yang tidak sesuai dengan implementasi aktual.*

*Dokumentasi ini dibuat berdasarkan audit menyeluruh terhadap seluruh struktur project `karhutla-threads-dashboard`. Semua nama file, fungsi, parameter, dan path telah diverifikasi langsung dari source code. Dokumentasi ini tidak berisi asumsi atau contoh generik yang tidak sesuai dengan implementasi aktual.*
7. **Semua halaman menggunakan pola `def render():` yang dipanggil di akhir file.** Ikuti pola ini untuk halaman baru.

---

*Dokumentasi ini dibuat berdasarkan audit menyeluruh terhadap seluruh struktur project `karhutla-threads-dashboard`. Semua nama file, fungsi, parameter, dan path telah diverifikasi langsung dari source code. Dokumentasi ini tidak berisi asumsi atau contoh generik yang tidak sesuai dengan implementasi aktual.*
- [ ] Tidak ada fungsi stub yang dipanggil tanpa penanganan `None`.
- [ ] Semua import menggunakan path yang benar (`from src import ...`).
- [ ] Jika mengubah `src/config.py`, verifikasi semua halaman masih tampil dengan benar.
- [ ] Tidak ada file besar atau sensitif yang di-commit ke git.

---

## Catatan Penting untuk Developer

1. **Jangan mengubah struktur project tanpa alasan yang jelas.** Semua path di `src/config.py` tergantung pada struktur folder saat ini.
2. **Semua perubahan di `src/config.py` berlaku global** karena design system terpusat di sana.
3. **Fungsi stub di `src/eda.py`, `src/cooccurrence.py`, `src/topic_modeling.py`, dan `src/comment_explorer.py` belum mengembalikan data aktual.** Jangan mengandalkan nilai kembaliannya untuk produksi sebelum diimplementasikan.
4. **`render_heatmap` di `src/visualization.py` memiliki bug pemanggilan `_show()` ganda.** Perbaikan disarankan sebelum menggunakan heatmap secara luas.
5. **`render_wordcloud` tidak mendukung parameter `key` ke `st.pyplot`.** Jika Anda melewatkan `key`, akan terjadi error.
6. **Tidak ada file `app.py` atau `main.py` terpisah di luar root.** Entry point adalah `app.py` di root project.
7. **Semua halaman menggunakan pola `def render():` yang dipanggil di akhir file.** Ikuti pola ini untuk halaman baru.

---

*Dokumentasi ini dibuat berdasarkan audit menyeluruh terhadap seluruh struktur project `karhutla-threads-dashboard`. Semua nama file, fungsi, parameter, dan path telah diverifikasi langsung dari source code. Dokumentasi ini tidak berisi asumsi atau contoh generik yang tidak sesuai dengan implementasi aktual.*
### 13.8 Global Styling Bertabrakan dengan Custom Styling

**Gejala:** Warna custom ter-overwrite oleh CSS global.

| Penyebab | Solusi |
|----------|--------|
| CSS global menggunakan class yang sama | Gunakan class unik dengan prefix nama halaman (lihat bagian [11. Custom Design Without Global Styling](#11-custom-design-without-global-styling)) |
| Spesifitas CSS global lebih tinggi | Gunakan `!important` di custom CSS atau tambahkan class induk yang lebih spesifik |

### 13.9 Error ketika menjalankan Modelling

**Gejala:** Error saat memanggil fungsi `src/topic_modeling.py`.

| Penyebab | Solusi |
|----------|--------|
| Semua fungsi adalah stub | `run_lda`, `preprocess_texts`, dll. masih mengembalikan `None` atau `[]`. Implementasikan terlebih dahulu (lihat bagian [6. Topic Modelling Module](#6-topic-modelling-module)) |
| `scikit-learn` tidak terinstal | `scikit-learn` sudah ada di `requirements.txt`. Jalankan `pip install -r requirements.txt` |

### 13.10 Error ketika Menghubungkan Hasil Modelling ke Halaman

**Gejala:** Halaman 4 tetap menampilkan placeholder meski fungsi modelling sudah diimplementasikan.

| Penyebab | Solusi |
|----------|--------|
| Halaman masih memanggil `render_placeholder_card` | Ganti blok placeholder dengan pemanggilan fungsi modelling aktual dan `render_*` chart |
| Fungsi modelling mengembalikan `None` | Periksa implementasi fungsi di `src/topic_modeling.py` dan pastikan return DataFrame, bukan `None` |

### 13.11 Dependency Belum Terinstal

**Gejala:** `ModuleNotFoundError: No module named 'wordcloud'`, `'plotly'`, `'sklearn'`, dll.

| Penyebab | Solusi |
|----------|--------|
| `pip install -r requirements.txt` belum dijalankan | Jalankan perintah tersebut di root project |
| Virtual environment tidak teraktivasi | Aktifkan `.venv\Scripts\Activate.ps1` |
### C. Optional (Fitur tambahan untuk pengembangan di masa depan)

| Nama File / Komponen | Fungsi yang Diharapkan | Alasan | Hubungan dengan File Lain | Prioritas |
|----------------------|------------------------|--------|---------------------------|-----------|
| `src/sentiment_analysis.py` | Modul analisis sentimen terpisah | Untuk analisis sentimen yang lebih mendalam | `pages/2_EDA.py`, `pages/6_Insights_Conclusion.py` | Rendah |
| `src/wordcloud_utils.py` | Utilitas WordCloud yang lebih dapat dikonfigurasi | `render_wordcloud` saat ini hardcoded banyak parameter | `pages/2_EDA.py` | Rendah |
| `pages/7_Export.py` | Halaman untuk export hasil analisis (CSV, PDF) | Fitur export belum ada | Semua halaman | Rendah |
| `src/auth.py` | Autentikasi dan izin pengguna | Untuk akses terbatas | `app.py` | Rendah |
| Unit tests (`tests/`) | Pengujian otomatis untuk fungsi-fungsi `src/` | Tidak ada pengujian saat ini | Semua fungsi `src/` | Rendah |
```
    --background: #EFF6FF;
    --text: #1E293B;
}
.blue-theme .kpi-card.kpi-dark {
    background: var(--primary) !important;
}
.blue-theme .page-title {
    color: var(--primary) !important;
}
.blue-theme .custom-card {
    background: var(--background);
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 16px;
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='blue-theme'>", unsafe_allow_html=True)

st.markdown("<h1 class='page-title'>Halaman dengan Tema Biru</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='custom-card'>
    Ini adalah kartu dengan desain independen, tidak mengikuti global CSS.
</div>
""", unsafe_allow_html=True)

render_kpi("Contoh KPI", 123, variant="dark")  # Akan tampil biru karena override

st.markdown("</div>", unsafe_allow_html=True)
```
Contoh:
```python
def generate_insight(df):
    if df is None:
        return "Data tidak tersedia."
    top_user = df["user_id"].value_counts().idxmax()
    return f"Pengguna paling aktif adalah {top_user}."

# Di halaman:
render_info_card("Insight Otomatis", generate_insight(df))
```

### 10.9 Menambahkan Tabel Interaktif

Gunakan `st.dataframe()` atau `st.table()`:

```python
import streamlit as st
st.dataframe(df, use_container_width=True)
```

Untuk pagination, gunakan fungsi `paginate` dari `src/comment_explorer.py` (setelah diimplementasikan).

### 10.10 Menambahkan Komponen UI Baru

Buat fungsi render baru di `src/visualization.py` mengikuti pola existing:

```python
def render_custom_box(title, content, color="#1B4332"):
    st.markdown(
        f"<div style='background-color:{color}; padding:12px; border-radius:8px; color:white;'>"
        f"<strong>{title}</strong><br>{content}</div>",
        unsafe_allow_html=True,
    )
```
Impor fungsi dari `src/eda.py`, `src/cooccurrence.py`, `src/topic_modeling.py`, atau `src/comment_explorer.py`:

```python
from src.eda import calculate_average_metric
rata2 = calculate_average_metric(df, "likes")
```

#### 6. Buat visualisasi

Gunakan fungsi chart dari `src.visualization.py`:

```python
from src.visualization import render_bar_chart, render_line_chart
render_bar_chart(df, x="kategori", y="jumlah", title="Contoh Chart")
```

#### 7. Atur styling

Gunakan class CSS global dari `assets/style.css` atau buat CSS khusus (lihat bagian [11. Custom Design Without Global Styling](#11-custom-design-without-global-styling)).

#### 8. Testing

Jalankan aplikasi dan buka halaman baru melalui sidebar:
```bash
streamlit run app.py
```

#### 9. Jalankan aplikasi

Pastikan tidak terdapat error pada console Streamlit.

| Fungsi                    | Parameter                                                                                                              | Deskripsi                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `render_process_flow`     | `(steps, title=None)`                                                                                                  | Menampilkan panel alur proses.                               |
| `render_sidebar_identity` | `(identity=None)`                                                                                                      | Menampilkan kartu identitas kelompok.                        |
| `render_bar_chart`        | `(data, x, y, title=None, horizontal=False, color=None, color_sequence=None, show_values=True, height=None, key=None)` | Menampilkan diagram batang menggunakan Plotly.               |
| `render_line_chart`       | `(data, x, y, title=None, color=None, markers=True, height=None, key=None)`                                            | Menampilkan diagram garis menggunakan Plotly.                |
| `render_pie_chart`        | `(data, names, values, title=None, hole=0.0, height=None, key=None)`                                                   | Menampilkan diagram lingkaran (Pie Chart).                   |
| `render_donut_chart`      | `(data, names, values, title=None, height=None, key=None)`                                                             | Menampilkan diagram Donut dengan `hole=0.55`.                |
| `render_histogram`        | `(data, x, title=None, nbins=None, height=None, key=None)`                                                             | Menampilkan histogram menggunakan Plotly.                    |
| `render_heatmap`          | `(data, x, y, z, title=None, height=None, key=None)`                                                                   | Menampilkan visualisasi Heatmap menggunakan Plotly.          |
| `render_wordcloud`        | `(data, text_col, title=None, height=None, key=None)`                                                                  | Menampilkan Word Cloud menggunakan Matplotlib dan WordCloud. |

**Catatan penting:**
- `render_bar_chart`, `render_pie_chart`, `render_donut_chart`, `render_histogram`, `render_line_chart`, `render_heatmap` **belum digunakan di manapun** kecuali `render_line_chart`, `render_histogram`, `render_heatmap`, `render_wordcloud` yang hanya digunakan di `pages/2_EDA.py`.
- `render_heatmap` memanggil `_show()` dua kali (baris 268-269 di `src/visualization.py`), menyebabkan chart duplikat.

### Cara Menambahkan Analisis Baru

1. Buat fungsi di modul yang sesuai (`src/eda.py`, `src/cooccurrence.py`, atau `src/topic_modeling.py`).
2. Impor fungsi di halaman `pages/X_*.py`.
3. Panggil fungsi dan tampilkan hasil dengan `render_*` dari `src.visualization.py`.

Contoh menambahkan fungsi distribusi sentimen di `src/eda.py`:
```python
def calculate_sentiment_distribution(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    if df is None or "sentimen" not in df.columns:
        return None
    return df["sentimen"].value_counts().reset_index()

    return lda, df_topik
```

#### Cara Menghubungkan Hasil Modelling ke Halaman

Di `pages/4_Topic_Analysis.py`, ganti blok `render_placeholder_card` dengan pemanggilan fungsi aktual:

```python
from src.topic_modeling import run_lda, coherence_scores, topic_proportion
from src.visualization import render_donut_chart, render_line_chart

tokens = preprocess_texts(df["comment_text"].tolist())
model, topik_df = run_lda(tokens, n_topics=4)

proporsi = topic_proportion(model, df)
render_donut_chart(proporsi, names="topik", values="proporsi", title="Proporsi Komentar Per Topik")

koherens = coherence_scores(range(2, 11))
render_line_chart(koherens, x="n_topik", y="koherens", title="Skor Koherens")
```
| Urutan | Section | Fungsi yang Digunakan | Keterangan |
|--------|---------|----------------------|------------|
| 1 | Page Title | `render_page_title("INSIGHT & KESIMPULAN")` | Judul halaman |
| 2 | Section Header | `render_section_header("Rangkuman Hasil Analisis", description="...")` | Judul + deskripsi |
| 3 | Layout 3 Kolom | `st.columns(3)` | Insight Utama, Temuan Penting, Kesimpulan |
| 4 | Info Card per Kolom | `render_info_card("Placeholder", "Isi...")` | 3 kartu, semua placeholder |
| 5 | Divider | `st.divider()` | Pemisah |
| 6 | Section: Integrasi | `render_section_header("Integrasi Hasil Analisis Lainnya")` + `render_info_card(...)` | Area fleksibel untuk dikembangkan |
| 7 | Data Notice | `render_data_notice(..., level="info")` | Catatan placeholder |

#### C. Cara Mengisi Konten Final

Ganti konten `render_info_card` dengan insight aktual:
```python
render_info_card(
    "Insight Utama",
    "Kebanyakan komentar mengarah pada kekhawatiran masyarakat terhadap penanganan karhutla di Kalimantan."
)
```

Untuk menambahkan lebih banyak insight, tambahkan kolom baru dengan `st.columns()` atau buat baris baru.

```
from src.topic_modeling import preprocess_texts, run_lda, coherence_scores, topic_proportion, top_words_per_topic
from src.visualization import render_donut_chart, render_line_chart, render_bar_chart

tokens = preprocess_texts(df["comment_text"].tolist())
model, topik_per_dokumen = run_lda(tokens, n_topics=4)

proporsi = topic_proportion(model, df)
render_donut_chart(proporsi, names="topik", values="proporsi", title="Proporsi Komentar Per Topik")

koherens_df = coherence_scores(range(2, 11))
render_line_chart(koherens_df, x="n_topik", y="koherens", title="Skor Koherens per Jumlah Topik")

top_words = top_words_per_topic(model, n=10)
render_bar_chart(top_words, x="bobot", y="kata", title="Top Kata per Topik", horizontal=True)
```

Setelah `src/cooccurrence.py` diimplementasikan, integrasi di halaman ini akan terlihat seperti:

```python
from src.cooccurrence import tokenize_texts, calculate_cooccurrence, get_top_pairs

tokens = tokenize_texts(df["comment_text"].tolist())
co_df = calculate_cooccurrence(tokens, min_cooccur=st.session_state.get("co_min", 2))
top_pairs = get_top_pairs(co_df, top_n=10)
```
```python
from src.visualization import render_bar_chart
render_bar_chart(top_pairs, x="jumlah", y="kata_a", title="Top 10 Pasangan Kata", horizontal=True)

top_users = df["user_id"].value_counts().head(10).reset_index()
top_users.columns = ["user_id", "jumlah"]
render_bar_chart(top_users, x="user_id", y="jumlah", title="Top 10 Pengguna", horizontal=True)
```

#### D. Panduan Editing Filter dan Input

Halaman EDA saat ini **tidak memiliki filter interaktif** (semua data ditampilkan tanpa filter). Untuk menambahkan filter:

```python
import streamlit as st

date_filter = st.date_input("Pilih tanggal", value=None)
if date_filter:
    df = df[df["_tanggal"] == pd.Timestamp(date_filter).date()]
```

#### E. Panduan Modelling dan Analisis

Halaman EDA **tidak memiliki modelling**. Semua analisis adalah deskriptif (mean, groupby, histogram). Untuk menambahkan modelling, lihat bagian [6. Topic Modelling Module](#6-topic-modelling-module) dan [7. Analytics Module](#7-analytics-module).
| `height` | None | Tinggi chart |
| `key` | None | Streamlit key |

Library: Plotly Express (`px.histogram`).

**Cara mengganti jenis chart:** Ubah pemanggilan di halaman. Mis. dari histogram ke bar chart:
```python
from src.visualization import render_bar_chart
render_bar_chart(df, x="kategori", y="jumlah", title="Distribusi", horizontal=False)
```

**Cara mengubah warna:** Edit file `src/visualization.py` pada baris 253, tepatnya parameter `color_discrete_sequence=[config.COLORS["red_orange"]]`.

| No. | Komponen              | Implementasi                                                    | Deskripsi                                                                                             |
| --- | --------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 5   | Divider               | `st.divider()`                                                  | Menampilkan pemisah visual.                                                                           |
| 6   | Kolom Turunan         | `df["_tanggal"]`, `df["_jam"]`, `df["_hari"]`, `df["_panjang"]` | Kolom dibuat di memori dan tidak disimpan ke file asli.                                               |
| 7   | Chart Row 1 (2 kolom) | WordCloud + Histogram                                           | Menampilkan WordCloud dan Histogram secara berdampingan.                                              |
| 8   | Chart Row 2 (2 kolom) | Line Chart (per hari) + Heatmap (hari × jam)                    | Menampilkan grafik tren harian dan distribusi aktivitas berdasarkan hari dan jam secara berdampingan. |
| 9   | Data Notice           | `render_data_notice(..., level="info")`                         | Menampilkan catatan terkait kolom turunan.                                                            |

**Konfigurasi komponen:**

```
n_raw,variant="red",compact=True,value_size="2.5rem",title_size="0.9rem",padding="12px 10px",)
```

#### E. Cara Menghapus atau Menyembunyikan Elemen

- Untuk menyembunyikan KPI tertentu: hilangkan blok `with colX:` atau komen baris `render_kpi(...)`.
- Untuk menghapus banner: komen baris `render_banner(...)`.
- Untuk menghapus process flow: komen baris `render_process_flow(...)`.


### **F. Contoh Implementasi: Mengganti Teks Placeholder**

Edit file `src/config.py`:

```
PROJECT_TITLE = "DASHBOARD BARU KAMU"BACKGROUND_TEXT = "Teks latar belakang baru di sini."OBJECTIVE_TEXT = "Teks tujuan baru di sini."
```

Tidak perlu mengubah `pages/1_Overview.py` karena halaman tersebut sudah mengambil nilai secara langsung dari `config.py`.

### **Class CSS dan Fungsinya**

| Class CSS                                   | Elemen HTML | Fungsi                                  |
| ------------------------------------------- | ----------- | --------------------------------------- |
| `.flow-dark` / `.flow-red` / `.flow-orange` | `<div>`     | Variasi warna pada langkah alur proses. |
| `.identity-card`                            | `<div>`     | Kartu identitas kelompok di sidebar.    |
| `.member-pill`                              | `<div>`     | Label anggota dalam identitas kelompok. |

### **Cara Menggunakan Global Styling di Halaman**

Semua halaman menggunakan fungsi `render_*` dari `src/visualization.py` yang sudah menerapkan class CSS di atas.

Contoh implementasi:

```
from src.visualization import (    render_page_title,    render_section_header,    render_kpi)render_page_title("JUDUL HALAMAN")          # Class .page-titlerender_section_header("Judul Section")       # Class .section-headerrender_kpi(    "Total Komentar",    1234,    variant="dark")                                            # Class .kpi-card.kpi-dark
```

### **Konfigurasi Global (**`src/config.py`**)**

#### **1. FONT_FAMILY dan FONT_URL**

Mengatur jenis huruf yang digunakan pada dashboard.

```
FONT_FAMILY = "Montserrat"FONT_URL = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap"
```

#### **2. LAYOUT**

Mengatur konfigurasi tata letak dan ukuran komponen.

| Kunci          | Nilai    | Keterangan                         |
| -------------- | -------- | ---------------------------------- |
| `page_layout`  | `"wide"` | Layout halaman Streamlit.          |
| `card_radius`  | `"8px"`  | Radius sudut kartu.                |
| `chart_height` | `380`    | Tinggi default chart dalam piksel. |

#### **3. CHART**

Mengatur tampilan default visualisasi Plotly.

| Kunci           | Nilai                                  | Keterangan                        |
| --------------- | -------------------------------------- | --------------------------------- |
| `font_family`   | `"Montserrat, sans-serif"`             | Jenis font chart.                 |
| `font_color`    | `"#1B4332"`                            | Warna teks chart.                 |
| `paper_bgcolor` | `"rgba(0,0,0,0)"`                      | Background luar chart transparan. |
| `plot_bgcolor`  | `"rgba(0,0,0,0)"`                      | Background area plot transparan.  |
| `margin`        | `{"l": 10, "r": 10, "t": 40, "b": 10}` | Pengaturan margin chart.          |

#### **4. EMPTY_VALUE**

```
EMPTY_VALUE = "—"
```

Menggunakan em dash (`—`) sebagai pengganti nilai yang tidak tersedia (`None`).

### **Alur Pemrosesan Data**

```
data/processed/comments_clean.csv
              ↓
       load_processed_data()
       (src/data_loader.py)
          @st.cache_data
              ↓
      Halaman Streamlit
        (pages/*.py)
              ↓
   Memanggil fungsi render_*
   (src/visualization.py)
              ↓
 Visualisasi Plotly / Matplotlib
           / WordCloud
```

### **Hubungan Antarfile**

**1. File utama (**`app.py`**)**

```
app.py
 ├── src/config.py
 │    └── PAGES, CSS_PATH, COLORS, dll.
 │
 ├── src.utils.load_css()
 │    └── Memuat assets/style.css
 │
 ├── src.visualization.render_sidebar_identity()
 │
 └── st.navigation([pages/...])
```

**2. File halaman (**`pages/*.py`**)**

Setiap halaman menggunakan modul berikut sesuai kebutuhan:

```
pages/X_*.py
 ├── src/config.py
 │    └── COLUMNS, COLORS, EMPTY_VALUE, dll.
 │
 ├── src/data_loader.py
 │    └── load_raw_data(), load_processed_data()
 │
 ├── src/preprocessing.py
 │    └── count_rows(), count_unique(), get_date_range()
 │
 └── src/visualization.py
      └── render_page_title(), render_kpi(),
          render_chart(), dll.
```