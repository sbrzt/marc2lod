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
    return " ".join(values).strip() if values else None


def parse_marc_records(
    data: Union[str, bytes],
    fields: Dict[str, Dict[str, str]]
    ) -> pd.DataFrame:

    if isinstance(data, (bytes, str)):
        if isinstance(data, str):
            data = data.encode("utf-8")
        data = io.BytesIO(data)
    records = marcxml.parse_xml_to_array(data)
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
                df[col] = df[col].apply(func)
            else:
                func = CLEANING_FUNCTIONS[func_name["func"]]
                kwargs = {
                    k: v for k, v in func_name.items() if k != "func"
                }
                df[col] = df[col].apply(lambda x: func(x, **kwargs))
    return df



