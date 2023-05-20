import os, time
import internetarchive as ia

# Define the name of the collection on Internet Archive
collection_name = "darwinslibrary"

# Create error log
error_log = open('bpl-marcs-errors.log', 'a')

# Define the path where the files will be saved
save_path = "marc-files"

# Create the directory if it doesn't exist
if not os.path.exists(save_path):
    os.mkdir(save_path)

# Change the working directory to the save_path directory
os.chdir(save_path)

# Search for items in the collection and download the MARC records
items = ia.search_items(f'collection:{collection_name}')
for item in items:
    identifier = item["identifier"]

    # Download the MARCXML record for the item
    try:
        xml_files = ia.download(identifier, formats=["MARC"])
    # If there is a error, write it to the error log
    except Exception as e:
        error_log.write(f"Could not download {identifier} because of error: {e}\n")
        print("There was an error; writing to log.")
    else:
        print(f"Downloading {identifier}...")
        time.sleep(1)
    
    for idx, xml_file in enumerate(xml_files):
        # Move the XML file to the desired location and remove the containing folder
        new_file_path = os.path.join(save_path, f"{identifier}_{idx+1}.xml")
        os.rename(xml_file.name, new_file_path)
        print(f"File downloaded: {new_file_path}")