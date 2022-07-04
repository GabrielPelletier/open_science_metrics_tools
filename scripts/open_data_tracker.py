
# Import necessary python modules
import requests
import json

ACCESS_TOKEN = 'Hz7TbXbi3Uipnkt9BaH9kTsg39RbebUvhWXT3qNav8topafVhXSPHdlWlAJw '

paper_doi = '"10.1371/journal.pone.0190005"'
#paper_doi = '"10.1371/journal.pone.0190006"'

# Query Zenodo for a dataset linked with the publication's DOI (simple search using the publication's DOI)
response = requests.get('https://zenodo.org/api/records',
                        params={'q': paper_doi,
                                'access_token': ACCESS_TOKEN})

# Print results in the command window
print(response.json())

# Load results in a python dict
data = response.json()

# Check if there was a hit (anything returned?). If there is 1 or more hit, load the data doi(s) in new variable
data_doi = []
if len(data["hits"]["hits"]) == 0:
    print('No dataset found by Zenodo for Publication DOI ' + paper_doi)
else:
    print(str(len(data["hits"]["hits"])) + ' dataset(s) entry found in Zenodo for Publication DOI ' + paper_doi)
    for hit in data["hits"]["hits"]:
        data_doi.append(hit["doi"])

a = 0