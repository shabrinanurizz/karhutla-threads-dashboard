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

import networkx as nx
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

# Versi daftar stopword (dipakai halaman Co-occurrence untuk memastikan file ini sudah versi terbaru).
STOPWORDS_VERSION = 3

# Stopword tambahan hasil pengecekan dataset aktual: kata penghubung, kata ganti, sapaan,
# kata tanya, kata keterangan waktu/jumlah, kata gaul/singkatan, dan kata "platform" medsos
# yang masih lolos di kolom `text_clean`.
# Kalau di grafik masih ada kata sampah, tinggal tambahkan di sini.
_EXTRA_STOPWORDS = {
    # kata topik utama: terlalu dominan, muncul di hampir semua pasangan
    "karhutla", "kebakaran", "hutan", "lahan",
    # penunjuk, penghubung, preposisi
    "ini", "itu", "ni", "tu", "sini", "situ", "sana", "disini", "disana", "dari", "dalam", "dengan",
    "pada", "oleh", "bagi", "tanpa", "antara", "hingga", "sampai", "sejak", "selama", "setelah",
    "sebelum", "sambil", "ketika", "saat", "agar", "supaya", "sehingga", "maka", "jika", "kalau",
    "kalo", "bila", "bahwa", "karena", "krn", "sebab", "serta", "lalu", "kemudian", "terus", "trus",
    "tapi", "tetapi", "namun", "melainkan", "justru", "padahal", "walau", "meski", "meskipun",
    "terhadap", "kepada", "melalui", "menurut", "seperti", "sebagai", "yaitu", "yakni", "tersebut",
    "atas", "sekitar", "secara", "sementara", "akhirnya", "ternyata", "sebenarnya", "segala",
    "bukan", "tidak", "tak", "nggak", "enggak", "gak", "ga", "tdk", "belum", "jangan", "dll",
    # kata ganti, sapaan, panggilan
    "saya", "aku", "kamu", "kau", "anda", "kalian", "kami", "kita", "mereka", "dia", "ia", "beliau",
    "gue", "gua", "lu", "lo", "ku", "mu", "si", "sang", "para", "kak", "kakak", "ka", "kk", "bang",
    "mas", "mbak", "pak", "bu", "nak", "bro", "sis", "guys", "gaes", "teman",
    # kata tanya
    "bagaimana", "gimana", "kenapa", "mengapa", "kapan", "dimana", "kemana", "berapa", "siapa",
    # kata kerja bantu / kata keterangan umum
    "sudah", "udah", "uda", "sdh", "masih", "sedang", "pernah", "akan", "bakal", "mulai", "tetap",
    "lagi", "langsung", "malah", "cuma", "cuman", "hanya", "saja", "aja", "doang", "juga", "pun",
    "bisa", "harus", "harusnya", "perlu", "boleh", "mau", "ingin", "coba", "mari", "ayo", "yuk",
    "punya", "pakai", "ikut", "membuat", "menjadi", "jadi", "jd", "adalah", "ialah", "ada",
    "paling", "sangat", "sekali", "banget", "makin", "semakin", "cukup", "terlalu", "sering",
    "banyak", "sedikit", "semua", "semuanya", "seluruh", "setiap", "tiap", "satu", "kali",
    "memang", "emang", "emg", "betul", "benar", "beneran", "sumpah", "makanya", "mungkin",
    # kata ganti tanya/keterangan lain
    "sama", "biar", "lebih", "kayak", "kaya", "gitu", "gini", "begitu", "begini", "dulu", "tadi", "kemarin",
    "sekarang", "baru", "habis", "balik", "kembali", "masuk", "tinggal", "hal", "cara", "masa",
    "soal", "waktu", "hari", "tahun", "bulan", "jam",
    # kata kerja ucapan/persepsi yang terlalu umum
    "tahu", "lihat", "melihat", "terlihat", "bilang", "kata", "katanya", "suruh", "tanya",
    # partikel dan singkatan gaul
    "sih", "kan", "dong", "deh", "lah", "kah", "tuh", "nih", "dah", "loh", "lho", "kok", "mah",
    "eh", "ya", "yaa", "yah", "iya", "yg", "dgn", "lg", "pas", "nya", "wkwk", "wkwkwk", "haha",
    "hehe", "mohon", "tolong",
    # kata "platform" media sosial
    "repost", "share", "threads", "postingan", "komen", "utas", "story", "post", "wa", "ig",
    # stopword bahasa Inggris
    "the", "of", "to", "and", "in", "is", "a", "an", "it", "for", "on", "this", "that", "are", "be",
    "we", "you", "your", "i", "my", "me", "so", "up", "at", "by", "as", "or", "if", "but", "not",
    "no", "with", "from", "was", "were", "have", "has", "had", "do", "does", "did", "will", "can",
    "just", "all", "our", "out", "they", "them", "their", "he", "she", "his", "her", "its", "what",
    "when", "who", "how", "why", "there", "here", "more", "most", "very", "than", "then", "too",
    "about", "into", "over", "been", "being", "would", "could", "should", "please", "like", "real",
}
_STOPWORDS_ID = _STOPWORDS_ID | _EXTRA_STOPWORDS


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



def get_most_connected_word(cooccurrence_df: Optional[pd.DataFrame]) -> Optional[str]:
    """Kata dengan total kemunculan bersama terbesar (dipakai sebagai kata target default)."""
    if cooccurrence_df is None or len(cooccurrence_df) == 0:
        return None
    total = (
        cooccurrence_df.groupby("kata_a")["jumlah"].sum()
        .add(cooccurrence_df.groupby("kata_b")["jumlah"].sum(), fill_value=0)
    )
    return str(total.idxmax())


def build_network_graph(
    cooccurrence_df: Optional[pd.DataFrame], max_edges: int = 80
) -> Optional[nx.Graph]:
    """Bangun graph jaringan kata dari `max_edges` pasangan terkuat.

    Node = kata, edge = pasangan kata, atribut edge `weight` = jumlah kemunculan bersama.
    """
    if cooccurrence_df is None or len(cooccurrence_df) == 0:
        return None
    top = cooccurrence_df.nlargest(max_edges, "jumlah")
    graph = nx.Graph()
    for a, b, w in top[["kata_a", "kata_b", "jumlah"]].itertuples(index=False):
        graph.add_edge(a, b, weight=int(w))
    return graph


def build_target_graph(
    cooccurrence_df: Optional[pd.DataFrame],
    keyword: str,
    max_neighbors: int = 15,
    max_inner_edges: int = 20,
) -> Optional[nx.Graph]:
    """Sub-jaringan di sekitar `keyword`: tetangga terkuat + hubungan antar-tetangga.

    Graph yang dikembalikan menyimpan kata target di `graph.graph["center"]`.
    """
    if cooccurrence_df is None or len(cooccurrence_df) == 0 or not keyword:
        return None
    kw = keyword.lower().strip()
    df = cooccurrence_df
    ego = df[(df["kata_a"] == kw) | (df["kata_b"] == kw)].nlargest(max_neighbors, "jumlah")
    if len(ego) == 0:
        return None

    graph = nx.Graph(center=kw)
    neighbors = set()
    for a, b, w in ego[["kata_a", "kata_b", "jumlah"]].itertuples(index=False):
        graph.add_edge(a, b, weight=int(w))
        neighbors.update((a, b))
    neighbors.discard(kw)

    inner = df[df["kata_a"].isin(neighbors) & df["kata_b"].isin(neighbors)]
    for a, b, w in inner.nlargest(max_inner_edges, "jumlah")[["kata_a", "kata_b", "jumlah"]].itertuples(index=False):
        graph.add_edge(a, b, weight=int(w))
    return graph
