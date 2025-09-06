# src/clean.py

import pandas as pd
import re
from typing import Callable, Dict, List


def pattern_replace(
    value: str,
    patterns=None,
    replacement=""
    ) -> str:

    if pd.isna(value):
        return value
    s = str(value)
    for pattern in patterns or []:
        s = re.sub(pattern, replacement, s)
    return s.strip() or None


def pattern_extract(
    value: str,
    pattern=None,
    group=1
    ) -> str:

    if pd.isna(value):
        return value
    match = re.search(pattern, str(value))
    return match.group(group) if match else value


def normalize_unicode(value):
    if pd.isna(value): 
        return value
    return unicodedata.normalize("NFKC", str(value))


def to_lowercase(value):
    if pd.isna(value): 
        return value
    return str(value).lower()


CLEANING_FUNCTIONS: Dict[str, Callable] = {
    "pattern_replace": pattern_replace,
    "pattern_extract": pattern_extract,
    "to_lowercase": to_lowercase,
    "normalize_unicode": normalize_unicode,
}
