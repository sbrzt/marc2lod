# src/extract.py

import requests
from pymarc import marcxml
from io import BytesIO
from pathlib import Path


def extract_records(
    source: str, 
    source_type: str = "file"
    ):

    if source_type == "file":
        return fetch_marcxml_from_file(source)
    elif source_type == "url":
        return fetch_marcxml_from_url(source)
    elif source_type == "string":
        return fetch_marcxml_from_string(source)
    else:
        raise ValueError(f"Unknown source_type: {source_type}")


def fetch_marcxml_from_url(url: str):
    r = requests.get(url)
    r.raise_for_status()
    return marcxml.parse_xml_to_array(r.content)


def fetch_marcxml_from_file(path: str):
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
    


def fetch_marcxml_from_string(xml_bytes: bytes | str):
    if isinstance(xml_bytes, str):
        xml_bytes = xml_bytes.encode("utf-8")
    return marcxml.parse_xml_to_array(BytesIO(xml_bytes))


'''
def download_marcxml(
    collection_name: str, 
    save_path: str
    ) -> None:

    # Create the directory if it doesn't exist
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # Search for items in the collection
    items = ia.search_items(f'collection:{collection_name}')

    for item in items:

        # Get the item identifier
        identifier = item["identifier"]
        
        # Try to download the record with that identifier, in MARC format, at the `save_path` destination, and do not create a new folder for each file
        try:
            xml_files = ia.download(identifier, 
                                    formats=["MARC"], 
                                    verbose=True, 
                                    destdir=save_path,
                                    no_directory=True)

        # If there is a error, print it
        except Exception as e:
            print(e)
'''