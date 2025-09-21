# src/extract.py

import requests
import internetarchive as ia
from pymarc import marcxml
from io import BytesIO
from pathlib import Path
from tqdm import tqdm


def extract_records(
    source: str, 
    source_type: str = "file"
    ):

    if source_type == "file":
        return fetch_data_from_file(source)
    elif source_type == "url":
        return fetch_data_from_url(source)
    elif source_type == "string":
        return fetch_data_from_string(source)
    elif source_type == "internetarchive":
        return fetch_data_from_internetarchive(source)
    else:
        raise ValueError(f"Unknown source_type: {source_type}")


def fetch_data_from_url(url: str):
    r = requests.get(url)
    r.raise_for_status()
    return marcxml.parse_xml_to_array(r.content)


def fetch_data_from_file(path: str):
    path = Path(path)
    if path.is_dir():
        records = []
        for file in path.glob("*.xml"):
            with open(file, "rb") as f:
                records.extend(marcxml.parse_xml_to_array(f))
        return records
    else:
        with open(path, "rb") as f:
            return marcxml.parse_xml_to_array(f)
    

def fetch_data_from_string(xml_bytes: bytes | str):
    if isinstance(xml_bytes, str):
        xml_bytes = xml_bytes.encode("utf-8")
    return marcxml.parse_xml_to_array(BytesIO(xml_bytes))


def fetch_data_from_internetarchive(
    source: str
    ):

    records = []
    search = ia.search_items(f"collection:{source}")
    for result in tqdm(search):
        identifier = result["identifier"]
        try:
            item = ia.get_item(identifier)
            for f in item.get_files(formats=["MARC"]):
                url = f.url
                r = requests.get(url)
                r.raise_for_status()
                recs = marcxml.parse_xml_to_array(BytesIO(r.content))
                records.extend(recs)
        except Exception as e:
            print(f"Error for {identifier}: {e}")
    return records
