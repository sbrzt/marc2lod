import os
from pymarc import marcxml, MARCReader

# Define the list of fields to extract
fields_to_extract = [
    ('Identifier', '770', 'o'),
    ('Title', '245', 'a'),
    ('Author', '100', 'a'),
    ('Place of publication', '260', 'a'),
    ('Name of publisher', '260', 'b'),
    ('Date of publication', '260', 'c'),
    ('Edition', '250', 'a'),
    ('Physical Description', '300', 'a'),
    ('Series', '490', 'a'),
    ('ISBN/ISSN', '020', 'a')
]

# Define the path to the folder containing the MARCXML files
folder_path = 'marc-files'

# Iterate over the folders in the specified folder
for folder in os.listdir(folder_path):

    # Construct the path to the MARCXML file in the current folder
    file_path = os.path.join(folder_path, folder, folder + '_marc.xml')

    # Check if the file exists
    if os.path.isfile(file_path):
        # Open the MARCXML file
        with open(file_path, 'rb') as marc_file:
            records = marcxml.parse_xml_to_array(marc_file)

            values = {}
    
            # Iterate over the MARC records in the file
            for record in records:
                value = {}
                # Get the Title and Author fields from the record
                for field_name, field_label, subfield in fields_to_extract:
                    try:
                        value[field_name] = record[field_label][subfield]
                    except: None
                print(value)
                '''
                if record[field_label][subfield]:
                    value = {field_name: record[field_label][subfield]}
                elif record[field_label]:
                    value = {field_name: record[field_label]}
                print(value)
                '''