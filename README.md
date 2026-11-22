# Karhutla Social Media Dashboard

Dashboard interaktif untuk menganalisis komentar media sosial terkait
kebakaran hutan dan lahan (**karhutla**), dibangun dengan **Python** dan
**Streamlit**.

## Struktur proyek

```text
karhutla-threads-dashboard/
├── app.py                      # Entry point aplikasi (navigasi 6 halaman)
├── README.md
├── requirements.txt
├── .gitignore
│
├── pages/
│   ├── 1_Overview.py           # Halaman Overview (diimplementasikan)
│   ├── 2_EDA.py                # Halaman EDA (kerangka, data aktual)
│   ├── 3_Cooccurrence.py       # Halaman Co-occurrence (kerangka)
│   ├── 4_Topic_Analysis.py     # Halaman Topic Modeling (kerangka sintaks)
│   ├── 5_Comment_Explorer.py   # Halaman Comment Explorer (kerangka)
│   └── 6_Insights_Conclusion.py# Halaman Insight & Kesimpulan (placeholder)
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Konfigurasi global & design system
│   ├── data_loader.py          # Pemuatan dataset (st.cache_data)
│   ├── preprocessing.py        # Fungsi ringkasan data dasar
│   ├── eda.py                  # Kerangka fungsi analisis EDA
│   ├── cooccurrence.py         # Kerangka fungsi co-occurrence
│   ├── topic_modeling.py       # Kerangka sintaks topic modeling
│   ├── comment_explorer.py     # Kerangka fungsi comment explorer
│   ├── visualization.py        # Komponen visualisasi reusable lintas halaman
│   └── utils.py                # Utility umum (CSS, format angka, dll.)
│
├── assets/
│   └── style.css               # Desain dashboard (design system)
│
├── data/
│   ├── raw/                    # Data mentah (tidak diubah)
│   ├── processed/              # Hasil preprocessing
│   └── model_output/           # Hasil pemodelan (nanti)
│
└── notebooks/                  # Jupyter notebook eksplorasi (nanti)
```

## Cara menjalankan

1. Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
```

2. Pasang dependensi:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
streamlit run app.py
```

## Desain

Sistem desain tertulis di `src/config.py` (warna, font, path, navigasi) dan
diterapkan di `assets/style.css`. Komponen visualisasi reusable ada di
`src/visualization.py` sehingga dapat diimpor oleh semua halaman dan anggota
tim lainnya.

## Catatan data

- Dataset belum diubah; file asli berada di `data/raw/` dan hasil
  preprocessing di `data/processed/`.
- Jika dataset belum tersedia, halaman menampilkan pesan peringatan yang jelas,
  bukan angka dummy.
- Untuk Tahap 4 (EDA, Co-occurrence), isi `config.RAW_DATA_FILE` dan
  `config.PROCESSED_DATA_FILE` serta periksa kolom dataset sebelum
  mengimplementasikan analisis.

## Tahapan pengerjaan

1. Inspeksi dan fondasi (selesai)
2. Analisis 5 gambar referensi → design system (selesai)
3. Fondasi dan Overview (selesai)
4. EDA dan Co-occurrence (menunggu instruksi berikutnya)
5. Placeholder Topic Modeling dan Comment Explorer (selesai sebagai kerangka)
6. Pengujian

## Lisensi

Tentukan lisensi proyek sesuai kebutuhan tim.
