"""Modul analisis co-occurrence (Tahap 4 — diimplementasikan).

Logika perhitungan kemunculan bersama kata ada di sini (`src/cooccurrence.py`).
Tampilan dashboard ada di `pages/3_Cooccurrence.py`.

Semua fungsi diimplementasikan menggunakan dataset aktual dari
`data/processed/comments_clean.csv` (kolom `text_clean`). Tidak ada angka
hasil analisis yang dipersiapkan secara buatan.
"""

import re
from collections import Counter
from itertools import combinations
from typing import List, Optional

import pandas as pd

# Stopword Bahasa Indonesia (daftar dasar, tanpa dependensi eksternal seperti Sastrawi)
_STOPWORDS_ID = {
    "ada", "adalah", "adanya", "adapun", "agak", "agaknya", "akan", "aktif",
    "alasan", "ali", "amana", "apa", "apaan", "apabila", "apakah", "apalagi",
    "artinya", "asal", "asalkan", "atau", "ataupun", "awal", "awalnya",
    "bagai", "bagian", "bahkan", "banyak", "beberapa", "begini", "beginian",
    "begitu", "begitunya", "belum", "belumlah", "benar", "benarkah", "benarlah",
    "berada", "berakhirlah", "berdasarkan", "berikut", "berikutnya", "berjalan",
    "berarti", "berturut", "berturut-turut", "besar", "biasa", "biasanya",
    "bila", "bilakah", "bilalah", "boleh", "bolehkah", "bolehlah", "buat",
    "bukan", "bukankah", "bukanlah", "cuma", "dahulu", "dan", "dapat",
    "daripada", "dekat", "demi", "dengan", "depan", "di", "dia", "dialah",
    "diantara", "diantaranya", "dimana", "dipakai", "diperankan", "dirinya",
    "dua", "untuk", "ke", "keadaan", "keberadaan", "kemudian", "kira",
    "kira-kira", "kita", "kok", "kurang", "lagi", "lagian", "lain", "lainnya",
    "lamanya", "lebih", "lewat", "mana", "masih", "masihkah", "masing",
    "masing-masing", "mau", "mungkin", "namun", "nah", "nanti", "nya",
    "pada", "padahal", "pasti", "perlu", "saat", "sampai", "sana", "sangat",
    "se", "sebab", "saja", "sejak", "selain", "selalu", "selama", "selamanya",
    "semua", "sendiri", "sendirian", "seperti", "siapa", "suatu", "tahap",
    "tapi", "telah", "tentang", "tentu", "tiga", "tidak", "tidaklah",
    "walaupun", "yang", "yanglah"
}


def _clean_text(text: str) -> str:
    """Case folding dan hapus karakter non-alfabet (kecuali spasi)."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return text


def _remove_stopwords(tokens: List[str]) -> List[str]:
    """Buang stopword dan token terlalu pendek (panjang 1)."""
    return [t for t in tokens if t not in _STOPWORDS_ID and len(t) > 1]


def tokenize_texts(texts: List[str]) -> List[List[str]]:
    """Pisahkan teks menjadi daftar token per dokumen (cleansing + stopword removal).

    Args:
        texts: Daftar string teks komentar.

    Returns:
        Daftar daftar token per dokumen.
    """
    result: List[List[str]] = []
    for text in texts:
        cleaned = _clean_text(text)
        tokens = cleaned.split()
        tokens = _remove_stopwords(tokens)
        result.append(tokens)
    return result


def calculate_cooccurrence(
    tokens_per_doc: List[List[str]], min_cooccur: int = 2
) -> Optional[pd.DataFrame]:
    """Hitung kemunculan bersama pasangan kata dalam satu dokumen.

    Args:
        tokens_per_doc: Hasil tokenisasi per dokumen.
        min_cooccur: Minimal kemunculan bersama agar pasangan dicatat.

    Returns:
        DataFrame dengan kolom ['kata_a', 'kata_b', 'jumlah'], atau None jika
        input kosong atau tidak ada pasangan yang memenuhi min_cooccur.
    """
    if not tokens_per_doc:
        return None

    counter: Counter = Counter()
    for tokens in tokens_per_doc:
        unique_tokens = sorted(set(tokens))
        if len(unique_tokens) < 2:
            continue
        for pair in combinations(unique_tokens, 2):
            counter[pair] += 1

    if not counter:
        return None

    rows = [
        {"kata_a": a, "kata_b": b, "jumlah": count}
        for (a, b), count in counter.items()
        if count >= min_cooccur
    ]
    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values("jumlah", ascending=False).reset_index(drop=True)
    return df


def get_top_pairs(
    cooccurrence_df: Optional[pd.DataFrame], top_n: int = 10, keyword: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """Ambil pasangan kata teratas, opsi difilter oleh kata target.

    Args:
        cooccurrence_df: Hasil calculate_cooccurrence.
        top_n: Banyak pasangan teratas.
        keyword: Jika diisi, hanya pasangan yang mengandung kata ini.

    Returns:
        DataFrame terurut menurun, atau None jika tidak ada data.
    """
    if cooccurrence_df is None or len(cooccurrence_df) == 0:
        return None

    df = cooccurrence_df.copy()
    if keyword:
        kw = keyword.lower().strip()
        mask = (df["kata_a"].str.lower() == kw) | (df["kata_b"].str.lower() == kw)
        df = df[mask]

    if len(df) == 0:
        return None

    df = df.sort_values("jumlah", ascending=False).head(top_n).reset_index(drop=True)
    return df

