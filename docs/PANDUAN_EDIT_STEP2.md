# Panduan Edit — Step 2 (Overview & Bagian yang Harus Diedit)

Dokumen ini khusus untuk langkah ke-2: mengedit bagian-bagian yang perlu disesuaikan (judul, teks, identitas, workflow, penempatan komponen, filter, dll.) di dashboard Karhutla Threads sesuai 5 referensi layar (Overview, EDA, Co-occurrence, Modelling/Perbandingan Topik, Comment Explorer).

---

## 1. File yang Terlibat

| File | Peran Utama |
|------|-------------|
| `src/config.py` | Design system tunggal: judul, teks placeholder, identitas kelompok, workflow steps, navigasi, warna, font, layout, pemetaan kolom |
| `pages/1_Overview.py` | Halaman Overview; fungsi `render()`; helper `_format_periode()`; KPI "Periode Pengambilan Data" |
| `pages/2_EDA.py` | Halaman EDA (Exploratory Data Analysis) |
| `pages/4_Topic_Analysis.py` | Halaman Modelling / Perbandingan Topik |
| `src/visualization.py` | Semua fungsi `render_*` reusable + helper internal |
| `assets/style.css` | CSS class untuk `.kpi-title`, `.kpi-value`, `.kpi-card`, `.page-title`, `.section-header`, dll. |

---

## 2. Bagian yang Harus Diedit di `src/config.py`

Semua identitas dan teks utama terpusat di sini. Ganti semua nilai placeholder (`[PLACEHOLDER]`) dengan teks final.

### 2.1 Judul & Teks Utama

| Elemen | Lokasi di `config.py` | Contoh Placeholder | Keterangan |
|--------|----------------------|-------------------|------------|
| Judul proyek | `PROJECT_TITLE` | `"[PLACEHOLDER] JUDUL PROYEK"` | Tampil di halaman Overview via `render_page_title()` |
| Latar belakang | `BACKGROUND_TEXT` | `"[Placeholder] Isi latar belakang proyek di sini."` | Banner kiri via `render_banner()` |
| Tujuan | `OBJECTIVE_TEXT` | `"[Placeholder] Isi tujuan proyek di sini."` | Banner kanan via `render_banner()` |

### 2.2 Identitas Kelompok (Sidebar)

| Elemen | Lokasi di `config.py` | Contoh Placeholder | Keterangan |
|--------|----------------------|-------------------|------------|
| Mata kuliah | `GROUP_IDENTITY["course"]` | `"[Placeholder]"` | Sidebar identitas |
| Dosen | `GROUP_IDENTITY["lecturer"]` | `"[Placeholder]"` | Sidebar identitas |
| Anggota | `GROUP_IDENTITY["members"]` | `["NAMA - NIM"] * 5` | Sidebar identitas (5 orang) |

### 2.3 Langkah Alur (Workflow)

| Elemen | Lokasi di `config.py` | Contoh | Keterangan |
|--------|----------------------|--------|------------|
| Workflow steps | `WORKFLOW_STEPS` | list of `(label, ikon, variant)` | 8 langkah via `render_process_flow()` |

Contoh saat ini:
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

### 2.4 Navigasi Halaman (Sidebar)

| Elemen | Lokasi di `config.py` | Keterangan |
|--------|----------------------|------------|
| Daftar halaman | `PAGES` | List dict dengan `path`, `label`, `icon`. Sesuai urutan sidebar. |

### 2.5 Desain System (Warna, Font, Layout)

| Elemen | Lokasi di `config.py` | Keterangan |
|--------|----------------------|------------|
| Warna | `COLORS` | Hex untuk green_dark, red_orange, orange, amber, cream, dll. |
| Font | `FONT_FAMILY`, `FONT_URL` | Default "Montserrat" |
| Layout | `LAYOUT` | `page_layout`, `card_radius`, `chart_height` |
| Chart | `CHART` | font_family, font_color, bgcolor, margin |

---
## 3. Nama Fungsi Render (`src/visualization.py`)

Semua fungsi diimpor dari `src.visualization`. Gunakan untuk komponen standar agar konsisten di semua halaman.

| Fungsi | Signature | Kegunaan |
|--------|-----------|----------|
| `render_page_title` | `(title, accent=False)` | Judul halaman besar (`<h1>`). `accent=True` untuk warna oranye (Overview). |
| `render_section_header` | `(title, description=None)` | Judul section (`<h3>`) + deskripsi opsional (`<p>`). |
| `render_kpi` | `(title, value, delta=None, variant="dark", compact=False)` | Kartu KPI berwarna. |
| `render_info_card` | `(title, content, variant="light")` | Kartu teks biasa (info-light / info-dark). |
| `render_banner` | `(left, right)` | Banner hijau berisi 2 kartu (digunakan LATAR BELAKANG & TUJUAN). |
| `render_process_flow` | `(steps, title=None)` | Panel alur proses 8 langkah. |
| `render_data_notice` | `(message, level="info")` | Pesan data belum tersedia (info / warning). |
| `render_pill_label` | `(text, variant="dark")` | Label pill berwarna. |
| `render_badge` | `(text, variant="red")` | Badge kecil (kembalikan string HTML). |
| `render_placeholder_card` | `(title, message=...)` | Kartu kosong untuk area belum diimplementasikan. |

### Chart functions
| Fungsi | Signature |
|--------|-----------|
| `render_bar_chart` | `(data, x, y, title=None, horizontal=False, ...)` |
| `render_line_chart` | `(data, x, y, title=None, ...)` |
| `render_pie_chart` | `(data, names, values, title=None, hole=0.0, ...)` |
| `render_donut_chart` | `(data, names, values, title=None, ...)` |
| `render_histogram` | `(data, x, title=None, ...)` |
| `render_heatmap` | `(data, x, y, z, title=None, ...)` |
| `render_wordcloud` | `(data, text_col, title=None, ...)` |

### Variant `render_kpi`
- `"dark"` → hijau (`#1B4332`)
- `"red"` → oranye-merah (`#D94A05`)
- `"orange"` → kuning-oranye (`#F58E0A` / amber)

### Parameter `compact=True`
Untuk kartu lebih kecil (nilai jadi `2rem`, judul jadi `0.85rem`). Cocok untuk KPI dengan teks panjang seperti tanggal.

---
## 4. Cara Tanpa Render / Ngolah Sendiri (Manual)

Jika ingin menyesuaikan ukuran, warna, atau tata letak lebih bebas tanpa pakai fungsi `render_*`, gunakan `st.markdown` dengan HTML/CSS inline atau `st.metric`.

### Contoh: Nilai dengan font kecil (untuk tanggal periode)

```python
import streamlit as st

st.markdown(
    "<div style='font-size:0.75rem; font-weight:700; color:#fff; text-align:center;'>"
    "2-31 Agustus 2026</div>",
    unsafe_allow_html=True,
)
```

### Contoh: KPI manual lengkap

```python
st.markdown(
    "<div style='background:#1B4332; border-radius:22px; padding:22px 12px; "
    "text-align:center; color:#fff; min-height:170px; display:flex; "
    "flex-direction:column; justify-content:center;'>"
    "<div style='font-weight:800; font-size:3.6rem; line-height:1.05;'>1169</div>"
    "<div style='font-weight:700; font-size:1rem; margin-top:8px;'>"
    "Periode Pengambilan Data</div></div>",
    unsafe_allow_html=True,
)
```

### Kapan pakai manual?
- Saat perlu override ukuran font yang tidak tersedia lewat parameter `render_kpi` (mis. tanggal terlalu panjang).
- Saat ingin tata letak yang berbeda dari standar kartu.
- Saat ingin menambahkan animasi atau gaya CSS khusus.

---
## 5. Penyesuaian Penempatan per Halaman

Berdasarkan 5 referensi layar, berikut penempatan komponen yang diinginkan:

### 5.1 Halaman Overview (`pages/1_Overview.py`)

Urutan dari atas ke bawah:
1. Judul halaman besar (`render_page_title`)
2. Banner hijau berisi LATAR BELAKANG & TUJUAN (`render_banner`)
3. 4 KPI card (selaras dengan referensi)
4. Panel ALUR MANAJEMEN DAN ANALISIS DATA (`render_process_flow`)

**Catatan khusus untuk KPI "Periode Pengambilan Data":** Posisikan di kanan paling akhir (lihat referensi Overview). Jika teks tanggal terasa tidak muat atau terlalu besar, lihat bagian **6** di bawah ini.

### 5.2 Halaman EDA (`pages/2_EDA.py`)

- Tampilkan KPI: Rata-rata Likes, Rata-rata Shares, Rata-rata Replies (3 card di atas).
- **Hapus kata tambahan seperti "metrik"** yang tidak perlu agar tampilan bersih sesuai referensi EDA.
- Komponen berikutnya: WordCloud, Distribusi Panjang Komentar, Jumlah Komentar Per Hari, Aktivitas Hari x Jam.

### 5.3 Halaman Modelling / Perbandingan Topik (`pages/4_Topic_Analysis.py`)

- Judul: "PERBANDINGAN TOPIK"
- Bagian atas: Proporsi Komentar Per Topik (donut/pie) + Skor Koherens (line chart)
- **Filter Topik A & Topik B dipindahkan ke bawah** (hanya berlaku untuk bagian bawahnya saja, mis. tren jumlah komentar per hari dan perbandingan metrik topik).
- Slider lambda (`λ`) dengan desain khusus (lihat bagian 7).
- Bagian bawah: Tren Jumlah Komentar per hari + perbandingan metrik (Jumlah Komentar, Rata-rata Likes, Replies, Shares) untuk Topik A vs Topik B.

---
## 6. Kasus Khusus: Perkecil Font Tanggal "Periode Pengambilan Data"

Di `pages/1_Overview.py`, periode ditampilkan sebagai KPI ke-4:

```python
render_kpi(
    "Periode Pengambilan Data",
    _format_periode(*periode),
    variant="dark",
)
```

Masalah: string panjang (contoh "2-31 Agustus 2026") terasa tidak muat karena `.kpi-title` di `assets/style.css` berukuran `1rem` dan `.kpi-value` `3.6rem`.

### Solusi A: Pakai `compact=True` (direkomendasi, paling cepat)

```python
render_kpi(
    "Periode Pengambilan Data",
    _format_periode(*periode),
    variant="dark",
    compact=True,   # nilai jadi 2rem, judul jadi 0.85rem
)
```

### Solusi B: Override CSS di `assets/style.css`

Tambah class baru atau ubah `.kpi-title`:

```css
/* Lebih kecil untuk semua KPI */
.kpi-title { font-size: 0.75rem; }

/* Atau class khusus periode */
.kpi-periode .kpi-title { font-size: 0.7rem; }
.kpi-periode .kpi-value { font-size: 2.5rem; }
```

Catatan: Jika menggunakan class khusus, perlu menambahkan class tersebut di HTML KPI (modifikasi `render_kpi` atau render manual).

### Solusi C: Render Manual tanpa `render_kpi`

```python
st.markdown(
    f"<div style='font-size:0.8rem; font-weight:700; color:#fff; text-align:center;'>"
    f"{_format_periode(*periode)}</div>",
    unsafe_allow_html=True,
)
```

### Rekomendasi
Coba **Solusi A** (`compact=True`) dulu karena paling cepat dan tidak perlu sentuh CSS. Jika masih terasa besar, gabungkan dengan **Solusi B** (CSS lebih kecil).

## 7. Desain Filter Lambda (`λ`) — Halaman Modelling

Berdasarkan referensi layar Modelling, slider lambda diletakkan di kanan bawah dengan keterangan:

```
kasih penjelasan lambda singkat disini

λ  0      0.5      1
   |-------|-------|
   (slider)

top x kata topik A     top x kata topik B
```

Implementasi sederhana di `pages/4_Topic_Analysis.py`:

```python
import streamlit as st

st.markdown("kasih penjelasan lambda singkat disini")

lambda_val = st.slider(
    "λ",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    key="lambda_slider",
)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("top x kata topik A")
with col_b:
    st.markdown("top x kata topik B")
```

---

## 8. Troubleshooting: Error EDA saat `streamlit run`

Jika halaman EDA (`pages/2_EDA.py`) error saat dijalankan, periksa hal berikut:

1. **Import dan pemanggilan fungsi** — Pastikan `pages/2_EDA.py` mengimpor fungsi dari `src/eda.py` dengan benar dan memanggilnya dengan argumen yang sesuai.
2. **Pemetaan kolom** — Pastikan kolom yang digunakan (`likes`, `shares`, `replies`, `date`, `comment_text`) sesuai dengan `config.COLUMNS`.
3. **Data kosong** — Cek apakah ada chart yang merujuk ke DataFrame kosong atau kolom yang tidak ada. Fungsi `render_*` di `visualization.py` akan menampilkan `_empty_notice` jika data kosong, tetapi pemrosesan data di `src/eda.py` masih bisa error sebelum mencapai render.
4. **Tanggal** — Jika menggunakan `get_date_range` atau filtering tanggal, pastikan kolom tanggal sudah dalam format datetime.
5. **Jalankan ulang** — Setelah perbaikan, jalankan kembali:
   ```bash
   streamlit run pages/2_EDA.py
   ```
   atau
   ```bash
   streamlit run
   ```

---

## 9. Checklist Sebelum Simpan / Push

- [ ] `PROJECT_TITLE` sudah diganti teks final (tidak ada `[PLACEHOLDER]`)
- [ ] `BACKGROUND_TEXT` dan `OBJECTIVE_TEXT` sudah diisi teks final
- [ ] `GROUP_IDENTITY` (course, lecturer, members) sudah sesuai data asli
- [ ] `WORKFLOW_STEPS` sudah 8 langkah sesuai referensi desain
- [ ] Posisi komponen Overview sudah sesuai urutan referensi (judul → banner → KPI → process flow)
- [ ] KPI EDA tidak mengandung kata tambahan seperti "metrik" yang tidak perlu
- [ ] Filter Topik A / Topik B di halaman Modelling ditempatkan di bawah (hanya berlaku bagian bawah)
- [ ] Slider lambda (`λ`) sudah dipasang di halaman Modelling
- [ ] Font tanggal "Periode Pengambilan Data" sudah menyesuaikan (cek di layar berbagai lebar)
- [ ] Aplikasi masih bisa dijalankan (`streamlit run`) tanpa error, terutama halaman EDA

---

## 10. Panduan Edit Per Halaman (Rincian)

Berikut panduan lengkap bagaimana mengedit setiap halaman, file yang diedit, dan contoh kode sebelum/sesudah.

### 10.1 Sidebar (Semua Halaman) — Hapus `?` dari Judul

**File:** `src/config.py` baris 44  
**Keterangan:** `SIDEBAR_TITLE` digunakan di semua halaman, perubahan ini berlaku global.

**Sebelum:**
```python
SIDEBAR_TITLE = "DASHBOARD KARHUTLA (?)"  # placeholder, sesuai referensi desain
```

**Sesudah:**
```python
SIDEBAR_TITLE = "DASHBOARD KARHUTLA"  # sesuai referensi desain
```

---

### 10.2 Halaman Overview (`pages/1_Overview.py`)

**Urutan komponen (dari atas ke bawah):**
1. Judul halaman besar (`render_page_title`)
2. Banner hijau LATAR BELAKANG & TUJUAN (`render_banner`)
3. 4 KPI card
4. Panel ALUR MANAJEMEN DAN ANALISIS DATA (`render_process_flow`)

**Kasus khusus: Perkecil font tanggal "Periode Pengambilan Data"**  
Baris 72-78: KPI ke-4 (kanan paling akhir). Tambahkan `compact=True`:

```python
render_kpi(
    "Periode Pengambilan Data",
    _format_periode(*periode),
    variant="dark",
    compact=True,   # nilai jadi 2rem, judul jadi 0.85rem
)
```

---

### 10.3 Halaman EDA (`pages/2_EDA.py`)

**File yang diedit:** `pages/2_EDA.py` dan `src/visualization.py`

**A. Hapus kata "Metrik" dari label KPI**  
Baris 44:

**Sebelum:**
```python
render_pill_label("Metrik Interaksi", variant="orange")
```

**Sesudah:**
```python
render_pill_label("Interaksi", variant="orange")
```

**B. Perbaiki error `render_wordcloud` (`key` tidak didukung `st.pyplot`)**  
File `src/visualization.py` baris 277:

**Sebelum:**
```python
st.pyplot(fig_w, use_container_width=True, key=key)
```

**Sesudah:**
```python
st.pyplot(fig_w, use_container_width=True)
```

**Komponen EDA (dari atas ke bawah):**
- 3 KPI: Rata-rata Likes, Rata-rata Shares, Rata-rata Replies
- WordCloud
- Distribusi Panjang Komentar
- Jumlah Komentar Per Hari
- Aktivitas Hari x Jam

---

### 10.4 Halaman Modelling / Perbandingan Topik (`pages/4_Topic_Analysis.py`)

**File yang diedit:** `pages/4_Topic_Analysis.py`

**Posisi komponen (dari atas ke bawah):**
1. Judul: "PERBANDINGAN TOPIK"
2. Proporsi Komentar Per Topik (donut) + Skor Koherens (line chart) — side by side
3. **Divider**
4. **Pemilih Topik** (Topik A, Topik B, apply) ← dipindah ke sini, hanya berlaku komponen di bawahnya
5. **Divider**
6. KPI perbandingan Topik A vs Topik B (Jumlah Komentar, Rata-rata Likes, Replies, Shares)
7. **Divider**
8. Tren Jumlah Komentar per hari + Kontrol Model (λ) + top x kata Topik A/B

**A. Pindahkan filter Topik A/B ke bawah Proporsi & Skor Koherens**

Blok filter dipindah dari posisi asli (sebelum Proporsi) ke posisi baru (setelah Skor Koherens, sebelum KPI banding). Filter hanya mempengaruhi komponen di bawahnya (KPI banding, tren, top x kata), bukan donut atau skor koherens di atas.

**B. Filter lambda hanya untuk top x kata Topik A/B**  
Slider `λ` dan `render_kpi("top x kata topik A/B")` berada di `col_d` ("Kontrol Model (λ)") di bagian bawah, hanya terkait ke top x kata Topik A dan B. Tidak perlu perubahan struktural.

---

## 11. Catatan Penting

- Semua perubahan di `src/config.py` berlaku **global** ke seluruh halaman (karena design system terpusat di sini).
- `SIDEBAR_TITLE` ditampilkan di sidebar kiri setiap halaman.
- `render_wordcloud` di `src/visualization.py` tidak boleh melewatkan parameter `key` ke `st.pyplot` (tidak didukung).
- Setelah semua edit, jalankan `streamlit run` dan verifikasi tidak ada error, terutama di halaman EDA.


---