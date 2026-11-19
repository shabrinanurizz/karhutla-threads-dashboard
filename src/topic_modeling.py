"""Modul topic modeling (Tahap 4 — diimplementasikan).

Implementasi alur preprocessing hingga pemodelan LDA menggunakan scikit-learn
(CountVectorizer + LatentDirichletAllocation), yang sudah tercantum di
requirements.txt.

Alur pelaksanaan:

    teks -> cleaning/case folding -> stopword removal -> tokenisasi
        -> vektorisasi (CountVectorizer)
        -> LDA (n_topik) -> topik per dokumen
        -> proporsi komentar per topik & kata teratas per topik
        -> skor koherens untuk menentukan n_topik optimal

Semua fungsi diimplementasikan menggunakan dataset aktual dari
`data/processed/comments_clean.csv` (kolom `text_clean`). Tidak ada angka
hasil analisis yang dipersiapkan secara buatan.
"""

from typing import List, Optional, Tuple

import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from src.cooccurrence import tokenize_texts


def preprocess_texts(texts: List[str]) -> List[List[str]]:
    """Cleansing hingga tokenisasi teks komentar.

    Args:
        texts: Daftar string teks komentar.

    Returns:
        Daftar daftar token per dokumen.
    """
    return tokenize_texts(texts)


def run_lda(
    tokens_per_doc: List[List[str]], n_topics: int
) -> Tuple[Optional[object], Optional[pd.DataFrame]]:
    """Pelatihan model LDA.

    Args:
        tokens_per_doc: Daftar daftar token per dokumen (hasil preprocess_texts).
        n_topics: Jumlah topik yang diinginkan.

    Returns:
        (model, topik_per_dokumen) atau (None, None) jika input kosong.
        Model dilengkapi atribut X_ (matriks vektor) dan feature_names_
        agar dapat digunakan oleh fungsi turunan (coherence_scores,
        topic_proportion, top_words_per_topic).
    """
    if not tokens_per_doc:
        return None, None

    texts = [" ".join(tokens) for tokens in tokens_per_doc if tokens]
    if not texts:
        return None, None

    vectorizer = CountVectorizer(max_df=0.95, min_df=2)
    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics, random_state=42, learning_method="batch"
    )
    lda.fit(X)

    # Simpan referensi untuk fungsi turunan
    lda.X_ = X  # type: ignore[attr-defined]
    lda.feature_names_ = vectorizer.get_feature_names_out()  # type: ignore[attr-defined]

    topic_dist = lda.transform(X)
    topik_per_dokumen = topic_dist.argmax(axis=1)
    df_topik = pd.DataFrame({
        "topik": [f"Topik {i + 1}" for i in topik_per_dokumen]
    })

    return lda, df_topik


def coherence_scores(models_range) -> Optional[pd.DataFrame]:
    """Hitung skor koherens (proxy: -perplexity) untuk berbagai jumlah topik.

    Args:
        models_range: Iterable of (n_topik, model) tuples, atau list model LDA
                      di mana n_topik diambil dari model.n_components.

    Returns:
        DataFrame dengan kolom ['n_topik', 'koherens'], atau None jika kosong.
        Koherens didefinisikan sebagai negasi perplexity (semakin tinggi,
        semakin baik).
    """
    results = []
    for item in models_range:
        if isinstance(item, tuple) and len(item) == 2:
            n_topik, model = item
        else:
            model = item
            n_topik = getattr(model, "n_components", None)

        if model is None or n_topik is None:
            continue

        try:
            if hasattr(model, "X_"):
                perp = model.perplexity(model.transform(model.X_))
                koherens = float(-perp)
            else:
                koherens = None
        except Exception:
            koherens = None

        results.append({"n_topik": n_topik, "koherens": koherens})

    if not results:
        return None

    df = pd.DataFrame(results)
    df = df.sort_values("n_topik").reset_index(drop=True)
    return df


def topic_proportion(model, df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Hitung proporsi komentar per topik.

    Args:
        model: Model LDA hasil run_lda.
        df: DataFrame komentar (digunakan hanya untuk jumlah total dokumen).

    Returns:
        DataFrame dengan kolom ['topik', 'proporsi'] untuk donut chart,
        atau None jika model/data tidak valid.
    """
    if model is None or df is None:
        return None
    if not hasattr(model, "X_"):
        return None

    topic_dist = model.transform(model.X_)
    topik_per_dokumen = topic_dist.argmax(axis=1)
    n_topics = model.n_components
    total = len(topik_per_dokumen)

    import pandas as _pd
    counts = _pd.Series(topik_per_dokumen).value_counts().sort_index()

    rows = []
    for i in range(n_topics):
        count = int(counts.get(i, 0))
        proporsi = count / total if total > 0 else 0.0
        rows.append({"topik": f"Topik {i + 1}", "proporsi": proporsi})

    return _pd.DataFrame(rows)


def top_words_per_topic(model, n: int = 10) -> Optional[pd.DataFrame]:
    """Ambil n kata teratas dengan bobot tertinggi per topik.

    Args:
        model: Model LDA hasil run_lda.
        n: Banyak kata teratas per topik.

    Returns:
        DataFrame dengan kolom ['topik', 'kata', 'bobot'],
        atau None jika model tidak valid.
    """
    if model is None:
        return None
    if not hasattr(model, "feature_names_"):
        return None

    feature_names = model.feature_names_
    rows = []
    for topik_idx, topic in enumerate(model.components_):
        top_indices = topic.argsort()[-n:][::-1]
        for idx in top_indices:
            rows.append({
                "topik": f"Topik {topik_idx + 1}",
                "kata": feature_names[idx],
                "bobot": float(topic[idx]),
            })

    if not rows:
        return None

    return pd.DataFrame(rows)

