import json, string, re

# Load JSON data
with open("data.json", "r") as f:
    data = json.load(f)

def split_author(author_str):
    # Split the author string into name and surname parts
    if "," in author_str:
        surname, name = author_str.split(",", 1)
        return name.strip().rstrip(string.punctuation), surname.strip().rstrip(string.punctuation)
    else:
        return "", author_str.strip()
    
# Clean the text data
def clean_text(text):
    # Remove any punctuation marks
    cleaned_text = re.sub(r'[^\w\s]+(?<!&)+(?<!-)', '', text.rstrip())
    # Remove any leading or trailing whitespaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text

# Process the data by cleaning the text fields
for item in data:
    try:
        item["title"] = clean_text(item["title"])
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
