# src/transform.py

import pandas as pd
from pymarc import marcxml
from typing import Union, Dict, Any, List
import io
import sys
from src.clean import CLEANING_FUNCTIONS


def extract_field(
    record, 
    spec: Union[str, Any]
    ) -> List[str]:
    
    tag = str(spec.get("tag"))
    code = str(spec.get("code", None))
    values = []
    if not tag:
        return None
    for field in record.get_fields(tag):
        if code:
            values.extend(field.get_subfields(code))
        else:
            values.append(field.data)
    if not values:
        return None
    return values if len(values) > 1 else values[0]


def parse_records(
    records: List,
    fields: Dict[str, Dict[str, str]]
    ) -> pd.DataFrame:

    rows = [
        {
            col: extract_field(record, spec) for col, spec in fields.items()
        }
        for record in records
    ]
    df = pd.DataFrame(rows)
    for col, spec in fields.items():
        for func_name in spec.get("cleaning", []):
            if isinstance(func_name, str):
                func = CLEANING_FUNCTIONS[func_name]
                df[col] = df[col].apply(
                    lambda x: [func(v) for v in x] if isinstance(x, list) else func(x)
                )
            else:
                func = CLEANING_FUNCTIONS[func_name["func"]]
                kwargs = {
                    k: v for k, v in func_name.items() if k != "func"
                }
                df[col] = df[col].apply(
                    lambda x: [func(v, **kwargs) for v in x] if isinstance(x, list) else func(x, **kwargs)
                )
    return df
