'''
Data cleaning and processing can be done at various stages in the workflow, depending on the specific requirements of your project and the nature of the data you are working with. Here are some options for where you could clean and process the data in your workflow:

Clean the data before loading it into Python: If the data in your JSON file contains a lot of extraneous punctuation and spaces, you may want to clean it up before loading it into Python. You could use a tool like Microsoft Excel or Google Sheets to remove any unwanted characters and ensure that the data is formatted consistently. Once you have cleaned the data, you can export it as a new JSON file and load it into Python using the json module.

Clean the data as you load it into Python: If you prefer to handle data cleaning within your Python script, you could add some code to remove any unwanted characters and format the data consistently as you load it into your CitationGenerator objects. For example, you could use the strip() method to remove leading and trailing spaces, and the replace() method to remove any unwanted punctuation.

Handle missing data within the CitationGenerator class: If some of the data in your JSON file is missing or incomplete, you may want to add some logic within the CitationGenerator class to handle these cases. For example, you could add an if statement to check whether a required field (e.g. the author or title)is missing, and provide a default value if needed.

-

If you want to further process the data (e.g. splitting the author field into name and surname), it's up to you whether to do it as you load the data into Python or within the CitationGenerator class. Here are some factors to consider when making this decision:

Reusability: If you plan to reuse the CitationGenerator class for other projects, it may be more useful to keep the class focused on generating citations and handle data processing elsewhere. This would make the class more versatile and reusable.

Complexity: If the data processing required is relatively simple and straightforward (e.g. splitting a string into two parts), it may be easiest to do it within the CitationGenerator class. On the other hand, if the processing is more complex (e.g. involves multiple steps or requires external libraries), it may be better to handle it outside the class.

Modularity: If you want to keep your code modular and flexible, you could create a separate function or module to handle the data processing. This would allow you to reuse the processing code in other parts of your project, or even in other projects.
'''

import json

class CitationGenerator:
    def __init__(self, 
                 author="", 
                 title="", 
                 placeOfPublication="", 
                 publisher="",
                 dateOfPublication="",
                 edition="",
                 extent="",
                 isbn=""):
        self.author = author
        self.title = title
        self.placeOfPublication = placeOfPublication
        self.publisher = publisher
        self.dateOfPublication = dateOfPublication
        self.edition = edition
        self.extent = extent
        self.isbn = isbn

    def printMLA(self):
        '''
        Author's Last Name, First Name. Title of Book. Publisher, Publication Year.
        '''
        print(f"""{self.author if self.author else 'SURNAME, NAME'}. {self.title if self.title else 'TITLE'}. {self.publisher if self.publisher else 'PUBLISHER'}, {self.dateOfPublication if self.dateOfPublication else 'DATE'}""")

# Open the JSON file
with open('data.json') as file:
    data = json.load(file)

# Create a list of CitationGenerators
citations = []
for obj in data:
    citation = CitationGenerator(obj.get('author'), 
                              obj.get('title'), 
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