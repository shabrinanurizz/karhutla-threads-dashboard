"""Modul Comment Explorer.

Logika filtering, pencarian, ringkasan statistik, dan pagination
untuk halaman `pages/5_Comment_Explorer.py`.
"""

import math
from typing import Optional, Sequence, Tuple

import pandas as pd

from src import config


def _get_col(df: pd.DataFrame, config_key: Optional[str], fallbacks: Sequence[str]) -> Optional[str]:
    """Mencari nama kolom di DataFrame berdasarkan config.COLUMNS atau nama umum."""
    if config_key and hasattr(config, "COLUMNS"):
        mapped = config.COLUMNS.get(config_key)
        if mapped and mapped in df.columns:
            return mapped

    lower_map = {col.lower(): col for col in df.columns}
    for name in fallbacks:
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return None


def filter_comments(
    df: Optional[pd.DataFrame],
    date_range: Optional[Tuple[object, object]] = None,
    topic: Optional[str] = None,
    query: Optional[str] = None,
) -> Optional[pd.DataFrame]:
    """Filter komentar berdasarkan rentang tanggal, topik, dan pencarian teks."""
    if df is None:
        return None
    if df.empty:
        return df.copy()

    result = df.copy()

    # 1. Filter rentang tanggal
    if date_range is not None and len(date_range) == 2:
        start_date, end_date = date_range
        date_col = _get_col(result, "date", ("date", "tanggal", "created_at", "timestamp"))
        if date_col is not None and (start_date is not None or end_date is not None):
            parsed_dates = pd.to_datetime(result[date_col], errors="coerce")
            mask = parsed_dates.notna()
            if start_date is not None:
                mask &= parsed_dates.dt.date >= pd.to_datetime(start_date).date()
            if end_date is not None:
                mask &= parsed_dates.dt.date <= pd.to_datetime(end_date).date()
            result = result[mask]

    # 2. Filter topik
    if topic is not None and str(topic).strip() != "":
        topic_col = _get_col(result, "topic", ("topic", "topik", "dominant_topic", "topic_label"))
        if topic_col is not None:
            result = result[result[topic_col].astype(str).str.strip() == str(topic).strip()]

    # 3. Filter kata kunci pada teks komentar
    if query is not None and str(query).strip() != "":
        text_col = _get_col(result, "text", ("comment_text", "komentar", "text", "text_clean"))
        if text_col is not None:
            keyword = str(query).strip()
            result = result[
                result[text_col].astype(str).str.contains(keyword, case=False, regex=False, na=False)
            ]

    return result


def summary_stats(df: Optional[pd.DataFrame]) -> dict:
    """Ringkasan statistik komentar untuk ditampilkan di panel kiri."""
    if df is None or df.empty:
        return {
            "total": None,
            "topik_terbanyak": None,
            "rata_rata_likes": None,
        }

    total = int(len(df))

    # Topik terbanyak
    topik_terbanyak = None
    topic_col = _get_col(df, "topic", ("topic", "topik", "dominant_topic", "topic_label"))
    if topic_col is not None:
        valid_topics = df[topic_col].dropna().astype(str).str.strip()
        valid_topics = valid_topics[valid_topics != ""]
        if not valid_topics.empty:
            topik_terbanyak = str(valid_topics.mode().iloc[0])

    # Rata-rata likes
    rata_rata_likes = None
    likes_col = _get_col(df, "likes", ("likes", "like_count", "like"))
    if likes_col is not None:
        numeric_likes = pd.to_numeric(df[likes_col], errors="coerce").dropna()
        if not numeric_likes.empty:
            rata_rata_likes = round(float(numeric_likes.mean()), 1)

    return {
        "total": total,
        "topik_terbanyak": topik_terbanyak,
        "rata_rata_likes": rata_rata_likes,
    }


def paginate(
    df: Optional[pd.DataFrame], page: int = 1, page_size: int = 10
) -> Tuple[Optional[pd.DataFrame], int]:
    """Paginate DataFrame untuk tampilan tabel komentar."""
    if df is None:
        return None, 0
    if df.empty:
        return df.copy(), 0

    safe_size = max(1, int(page_size))
    total_pages = math.ceil(len(df) / safe_size)
    safe_page = max(1, min(int(page), total_pages))

    start_idx = (safe_page - 1) * safe_size
    end_idx = start_idx + safe_size
    return df.iloc[start_idx:end_idx].copy(), total_pages