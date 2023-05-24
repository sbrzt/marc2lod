import json, string, re

# Load JSON data
with open("data.json", "r") as f:
    data = json.load(f)

# Process the data by cleaning the text fields
for item in data:
    try:
        item["title"] = clean_text(item["title"])
        item["subtitle"] = clean_text(item["subtitle"])
        item["authorName"] = split_author(item["author"])[0]
        item["authorSurname"] = split_author(item["author"])[1]
        item["author"] = clean_text(item["author"])
        item["publisher"] = clean_text(item["publisher"])
        item["placeOfPublication"] = clean_text(item["placeOfPublication"])
        item["dateOfPublication"] = clean_text(item["dateOfPublication"])
    except:
        print(f"Missing data in {item}")

# Print the processed data
with open("data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
