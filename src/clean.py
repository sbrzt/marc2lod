# src/clean.py

import pandas as pd
import re
from typing import Callable, Dict, List


def clean_trailing_punctuation(value: str) -> str:
    if pd.isna(value):
        return value
    return re.sub(r'[.,!\[\]?:;]+$', '', str(value)).strip()

def normalize_missing_value(value: str) -> str:
    if pd.isna(value):
        return value
    return re.sub(r'\[s\.n\.\]|\[s\.l\.\]|n\.d\.', '', str(value)).strip() or None

def strip_whitespace(value):
    if pd.isna(value): 
        return value
    return re.sub(r'\s+', ' ', str(value)).strip()

def normalize_unicode(value):
    if pd.isna(value): 
        return value
    return unicodedata.normalize("NFKC", str(value))

def remove_brackets(value):
    if pd.isna(value): 
        return value
    return re.sub(r'^\[|\]$', '', str(value))

def normalize_year(value):
    if pd.isna(value): 
        return value
    match = re.search(r'(\d{4})', str(value))
    return match.group(1) if match else value

def to_lowercase(value):
    if pd.isna(value): 
        return value
    return str(value).lower()

def replace_empty_with_none(value):
    if pd.isna(value): 
        return None
    if str(value).strip() == "":
        return None
    return value


CLEANING_FUNCTIONS: Dict[str, Callable] = {
    "strip_whitespace": strip_whitespace,
    "to_lowercase": to_lowercase,
    "normalize_unicode": normalize_unicode,
    "remove_brackets": remove_brackets,
    "clean_trailing_punctuation": clean_trailing_punctuation,
    "normalize_missing_value": normalize_missing_value,
    "replace_empty_with_none": replace_empty_with_none,
    "normalize_year": normalize_year,
}
