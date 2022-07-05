
import requests
import json

this_doi = "10.1093/cercor/bhac132"

# Query DataCite for a dataset linked with the publication's DOI (simple search using the publication's DOI)
query = 'https://api.datacite.org/dois?query=10.1093/cercor/bhac132'
response = requests.get(query)

# Print results in the command window
print(response.json())

# Load results in a python dict
data = response.json()

a = 0
