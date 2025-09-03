# src/transform.py

import os
import pandas as pd
import pymarc


def get_author(record):
    try:
        author = record['100']['a']
        return author
    except Exception as e:
        print(e)


def get_title(record):
    try:
        title = record['245']['a']
        return title
    except Exception as e:
        print(e)


def get_subtitle(record):
    try:
        subtitle = record['245']['b']
        return subtitle
    except Exception as e:
        print(e)


def get_pub_place(record):
    try:
        pub_place = record['260']['a']
        return pub_place
    except Exception as e:
        print(e)


def get_publisher(record):
    try:
        publisher = record['260']['b']
        return publisher
    except Exception as e:
        print(e)


def get_pub_date(record):
    try:
        pub_date = record['260']['c']
        return pub_date
    except Exception as e:
        print(e)


def get_note(record):
    try:
        notes = [note['a'] for note in record.get_fields('500')]
        return notes
    except Exception as e:
        print(e)


def get_ident(lst):
    try:
        for strng in lst:
            if strng.startswith('Identifier'):
                ident = strng[12:]
                return ident
    except Exception as e:
        print(e)


def get_alt_ident(lst):
    try:
        for strng in lst:
            if strng.startswith('Public number: '):
                ident = strng[15:]
                return ident
    except Exception as e:
        print(e)


def get_supp_material(record):
    try:
        supp_material = record['770']['o']
        return supp_material
    except Exception as e:
        print(e)


def get_supp_parent(record):
    try:
        supp_parent = record['772']['o']
        return supp_parent
    except Exception as e:
        print(e)


def parse_marc_records(
    path: str
    ) -> pd.DataFrame:

    data = []

    # Iterate over the folder
    for filename in os.listdir(path):

        # Construct the path to the MARCXML file in the current folder
        file_path = os.path.join(path, filename)

        # Check if the file exists at that path
        if os.path.isfile(file_path):
            
            # Open the MARCXML file and return the records within it as an array
            with open(file_path, 'rb') as marc_file:
                records = pymarc.marcxml.parse_xml_to_array(marc_file)
        
                # Iterate over the MARC records array and generate a dictionary for each record
                for record in records:
                    dct = {
                        'ID': get_ident(get_note(record)),
                        'ALT_ID': get_alt_ident(get_note(record)),
                        'AUTHOR': get_author(record),
                        'TITLE': get_title(record),
                        'SUBTITLE': get_subtitle(record),
                        'NOTE': ' '.join(get_note(record)),
                        'SUPP_MATERIAL': get_supp_material(record),
                        'SUPP_PARENT': get_supp_parent(record),
                        'PUB_PLACE': get_pub_place(record),
                        'PUBLISHER': get_publisher(record),
                        'PUB_DATE': get_pub_date(record)
                    }
                    data.append(dct)

    df = pd.DataFrame(data)
    return df

