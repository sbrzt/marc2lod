# tests/test_transform.py

import yaml
import os
import pandas as pd
from src.transform import parse_records


FIXTURE_FILE = "tests/fixtures/sample.xml"
CONFIG_FILE = "config.yaml"

def test_parse_records():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    fields = config["fields"]

    with open(FIXTURE_FILE, "r", encoding="utf-8") as f:
        xml_str = f.read()

    df = parse_records(xml_str, fields)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1

    row = df.iloc[0]

    assert row["ID"] == "12345"
    assert row["AUTHOR"] == "Charles Darwin"
    assert row["TITLE"] == "On the Origin of Species"
    assert row["SUBTITLE"] == "by Means of Natural Selection"
    assert row["PUB_PLACE"] == "London"
    assert row["PUBLISHER"] == "NaN"
    assert row["PUB_DATE"] == "1859"
    assert row["NOTE"] == "First edition"
    assert row["ALT_ID"] == "ALT-999"