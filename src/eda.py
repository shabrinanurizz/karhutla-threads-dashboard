
"""Modul analisis Exploratory Data Analysis (EDA)."""

import ast
from collections import Counter
from typing import Optional

import pandas as pd

from src import config


# Stopwords tambahan untuk membersihkan kata umum
CUSTOM_STOPWORDS = {
    "karhutla", "bakar", "kalimantan", "hutan", "lahan"
}


# Urutan hari untuk heatmap
URUTAN_HARI = [
    "Senin", "Selasa", "Rabu", "Kamis",
    "Jumat", "Sabtu", "Minggu",
]


def calculate_total_comments(df: Optional[pd.DataFrame]) -> Optional[int]:
    """Menghitung total komentar."""
    if df is None:
        return None

    return int(len(df))


def calculate_average_metric(
    df: Optional[pd.DataFrame],
    column: str
) -> Optional[float]:
    """Menghitung rata-rata metrik engagement."""
    if df is None or column not in df.columns:
        return None

    return float(pd.to_numeric(df[column], errors="coerce").mean())


def calculate_sentiment_distribution(df: Optional[pd.DataFrame]):
    """Placeholder distribusi sentimen."""
    if df is None:
        return None

    return None


def prepare_daily_comments(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Menghitung jumlah komentar setiap hari."""

    if df is None or df.empty:
        return pd.DataFrame(columns=["tanggal", "jumlah"])

    date_col = config.COLUMNS["date"]
    data = df.copy()

    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data = data.dropna(subset=[date_col])

    daily = (
        data.groupby(data[date_col].dt.date)
        .size()
        .reset_index(name="jumlah")
    )

    daily.columns = ["tanggal", "jumlah"]

    return daily


def prepare_hourly_activity(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Menghitung aktivitas komentar berdasarkan hari dan jam."""

    if df is None or df.empty:
        return pd.DataFrame(columns=["hari", "jam", "jumlah"])

    date_col = config.COLUMNS["date"]
    data = df.copy()

    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data = data.dropna(subset=[date_col])

    nama_hari = {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu",
    }

    data["hari"] = data[date_col].dt.dayofweek.map(nama_hari)
    data["jam"] = data[date_col].dt.hour

    activity = (
        data.groupby(["hari", "jam"])
        .size()
        .reset_index(name="jumlah")
    )

    activity["hari"] = pd.Categorical(
        activity["hari"],
        categories=URUTAN_HARI,
        ordered=True,
    )

    activity = activity.sort_values(["hari", "jam"])

    return activity


def prepare_comment_length(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Menghitung panjang komentar berdasarkan jumlah kata."""

    if df is None or df.empty:
        return pd.DataFrame(columns=["jumlah_kata"])

    text_col = config.COLUMNS["text_clean"]

    if text_col not in df.columns:
        return pd.DataFrame(columns=["jumlah_kata"])

    data = df[[text_col]].copy()

    data["jumlah_kata"] = data[text_col].apply(
        lambda x: len(x.split())
        if pd.notna(x) and str(x).strip()
        else None
    )

    return data.dropna(subset=["jumlah_kata"])[["jumlah_kata"]]


def prepare_wordcloud_data(
    token_df: Optional[pd.DataFrame]
) -> pd.DataFrame:
    """Menghitung frekuensi kata dan jumlah komentar unik per kata."""

    columns = ["kata", "frekuensi", "jumlah_komentar"]

    if (
        token_df is None
        or token_df.empty
        or "tokens" not in token_df.columns
    ):
        return pd.DataFrame(columns=columns)

    frequency = Counter()
    comment_counts = Counter()

    for item in token_df["tokens"].dropna():

        if isinstance(item, str):
            try:
                tokens = ast.literal_eval(item)
            except (ValueError, SyntaxError):
                tokens = item.split()
        else:
            tokens = item

        if not isinstance(tokens, (list, tuple)):
            continue

        words = [
            str(token).lower().strip()
            for token in tokens
            if str(token).strip()
            and str(token).lower().strip() not in CUSTOM_STOPWORDS
        ]

        # Frekuensi seluruh kemunculan kata
        frequency.update(words)

        # Jumlah komentar yang mengandung setiap kata
        comment_counts.update(set(words))

    if not frequency:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame([
        {
            "kata": word,
            "frekuensi": count,
            "jumlah_komentar": comment_counts[word],
        }
        for word, count in frequency.most_common(100)
    ])
