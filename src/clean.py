# src/clean.py

import pandas as pd
import re


def clean_trailing_punctuation(value):
    '''
    Clean trailing punctuation from each value in a DataFrame.

    Args:
        value (str): a string value contained in a DataFrame cell.

    Returns:
        value (str): a string containing the value cleaned from any existing trailing punctuation.
    '''
    try:
        value = re.sub(r'^[.,!\[\]?:;]|[.,!\[\]?:;]$', '', value)
        value = value.strip()
    except:
        None
    return value


def normalize_missing_value(value):
    '''
    Normalizes a missing value in a DataFrame into a None value.

    Args:
        value (str): a string value contained in a DataFrame cell.

    Returns:
        value (str): a string containing a None value if the input value contains "[s.n.]" or "n.d.".
    '''
    try:
        value = re.sub(r'\[s.n.\]|n.d.', 'NaN', value)
    except:
        None
    return value


def remove_additional_date(value):
    '''
    Normalizes a time period by considering only the start date.

    Args:
        value (str): a string value contained in a DataFrame cell.

    Returns:
        value (str): a string containing only a date.
    '''
    try:
        value_split = value.split('-')
        value = value_split[0]
    except:
        None
    return value


def apply_functions(
    df: pd.DataFrame
    ) -> pd.DataFrame:
    columns_to_clean = [
        'ID', 
        'ALT_ID', 
        'TITLE', 
        'NOTE', 
        'AUTHOR', 
        'PUBLISHER', 
        'PUB_PLACE', 
        'PUB_DATE'
    ]
    columns_to_normalize = ['PUB_PLACE', 'PUBLISHER', 'PUB_DATE']
    columns_to_remove_date = ['PUB_DATE']

    df[columns_to_clean] = df[columns_to_clean].map(clean_trailing_punctuation)
    df[columns_to_normalize] = df[columns_to_normalize].map(normalize_missing_value)
    df[columns_to_remove_date] = df[columns_to_remove_date].map(remove_additional_date)

    return df