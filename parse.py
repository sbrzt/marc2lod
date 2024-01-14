import os, json, string, re
from pymarc import marcxml

# Define the list of fields to extract: field 100 (Main Entry Personal Name), 
# 245 (Title Statement), 260 (Publication, Distribution, etc. (Imprint)), and 
# 300 (Physical Description)
fields_to_extract = [
    ('author', '100', 'a'),
    ('title', '245', 'a'),
    ('subtitle', '245', 'b'),
    ('publisher', '260', 'b'),
    ('dateOfPublication', '260', 'c'),
]

# Prepare the list of dictionaries
data = []

# Define the path to the folder containing the MARCXML files
folder_path = 'marc-files'

'''
def split_author(author_str):
    # Split the author string into name and surname parts
    if "," in author_str:
        surname, name = author_str.split(",", 1)
        return [name.strip().rstrip(string.punctuation), surname.strip().rstrip(string.punctuation)]
    else:
        return [author_str]
'''
    
# Clean the text data
def clean_text(text):
    # Remove any punctuation marks
    cleaned_text = re.sub(r'[^\w\s]+(?<!&)+(?<!-)', '', text.rstrip())
    # Remove any leading or trailing whitespaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text

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
                        print(f"Could not find {field_name}-{field_label}-{subfield} in record")
                    else:
                        print(f"Parsing...")

                # Popoulate the list of dictionaries
                data.append(value)

# Save the data as a JSON file
with open("data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
                