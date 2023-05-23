import json
from bdo import BibliographicDataObject

# Open the JSON file
with open('data.json') as file:
    data = json.load(file)

# Create a list of BibliographicDataObjects
citations = []
for obj in data:
    citation = BibliographicDataObject(obj.get('author'), 
                              obj.get('authorName'),
                              obj.get('authorSurname'),
                              obj.get('title'), 
                              obj.get('subtitle'),
                              obj.get('placeOfPublication'), 
                              obj.get('publisher'), 
                              obj.get('dateOfPublication'), 
                              obj.get('edition'), 
                              obj.get('extent'),
                              obj.get('isbn'))
    citations.append(citation)

# Print the list of CitationGenerators
for citation in citations:
    citation.printMLA()
    citation.printAPA()