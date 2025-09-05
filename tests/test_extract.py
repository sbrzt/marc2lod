# tests/test_extract.py

import os
import pytest
from src.extract import extract_records

FIXTURE_FILE = os.path.join(os.path.dirname(__file__), "fixtures", "sample.xml")

def test_extract_from_file():
    records = extract_records(FIXTURE_FILE, source_type="file")
    assert len(records) == 1
    assert records[0]["245"]["a"] == "On the Origin of Species"

def test_extract_from_string():
    xml_str = open(FIXTURE_FILE).read()
    records = extract_records(xml_str, source_type="string")
    assert len(records) == 1
    assert records[0]["100"]["a"] == "Charles Darwin."

