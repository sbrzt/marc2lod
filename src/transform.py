# src/transform.py

import pandas as pd
from pymarc import marcxml
from typing import Union, Dict, Any, List
import io
import sys


def extract_field(
    record, 
    spec: Union[str, Any]
    ) -> List[str]:
    
    tag = str(spec.get("tag"))
    code = str(spec.get("code"))

    values = []
    for field in record.get_fields(tag):
        if code:
            values.extend(field.get_subfields(code))
        else:
            values.append(field.data)

    return values


def parse_marc_records(
    data: Union[str, bytes],
    fields: Dict[str, Dict[str, str]]
    ) -> pd.DataFrame:

    if isinstance(data, (bytes, str)):
        if isinstance(data, str):
            data = data.encode("utf-8")
        data = io.BytesIO(data)

    records = marcxml.parse_xml_to_array(data)
    rows = []
    for record in records:
        row = {}
        for colname, spec in fields.items():
            vals = extract_field(record, spec)
            row[colname] = "; ".join(vals) if vals else None
        rows.append(row)
    
    return pd.DataFrame(rows)



