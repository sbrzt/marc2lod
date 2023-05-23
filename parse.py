import os, json, codecs
from pymarc import marcxml

# Create error log
error_log = codecs.open('parse-marc-error.log', 'w', encoding='utf-8')

# Define the list of fields to extract
fields_to_extract = [
    ('author', '100', 'a'),
    ('title', '245', 'a'),
    ('subtitle', '245', 'b'),
    ('edition', '250', 'a'),
    ('placeOfPublication', '260', 'a'),
    ('publisher', '260', 'b'),
    ('dateOfPublication', '260', 'c'),
    ('extent', '300', 'a'),
    ('physicalDetails', '300', 'b'),
    ('dimensions', '300', 'c'),
    ('publicationFrequency', '310', 'a'),
    ('contentType', '336', 'a'),
    ('mediaType', '337', 'a'),
    ('medium', '340', 'a'),
    ('accessibilityContent', '341', 'a'),
    ('series', '490', 'a'),
    ('note', '500', 'a'),
    ('preferredCitation', '524', 'a'),
    ('identifier', '770', 'o'),
    ('isbn', '020', 'a'),
    ('termsOfAvailability', '020', 'c'),
    ('qualifyingInformation', '020', 'q'),
    ('issn', '022', 'a'),
    ('lcControlNumber', '010', 'a'),
    ('holdingInstitution', '850', 'a'),
    ('location', '852', 'a')
]

# Prepare the list of dictionaries
data = []

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
    
            # Iterate over the MARC records in the file
            for record in records:
                value = {}
                # Get the Title and Author fields from the record
                for field_name, field_label, subfield in fields_to_extract:
                    try:
                        value[field_name] = record[field_label][subfield]
                    except Exception as e:
                        error_log.write(f"Could not find {field_name}-{field_label}-{subfield} in {record} because of error: {e}\n")
                        print(f"Could not find {field_name}-{field_label}-{subfield} in {record} because of error: {e}\n")
                    else:
                        print(f"Parsing...")

                # Popoulate the list of dictionaries
                data.append(value)

# Save the data as a JSON file
with open("data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
                