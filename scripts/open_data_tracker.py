# Python code to scrape online resources (via APIs) to find out whether
# publications are associated with an Open Dataset.
# So far searches for datasets indexed by Zenodo and DataCite
# Gabriel Pelletier, July 2022

# Import necessary python modules
import requests
import json
import os
from pandas import *

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Retrieve ACCESS TOKEN from environment variable (has to be set prior)
access_token = os.environ.get('ZENODO_API_ACCESS_TOKEN')

# Set paths and file names
data_dir = ROOT_DIR + '/data/'
publications_file_name = 'master_list'
publications_file_path = data_dir + publications_file_name + '.csv'

# load publication list for which to retrieve dataset information
publications_df = read_csv(publications_file_path)

is_dataset_column = []
data_dois_column = []

# Loop over publications
for index, row in publications_df.iterrows():

    # Will become one if a dataset is found for this publications
    is_dataset = 0

    this_doi = '"' + row['doi'] + '"'
    this_title = row['title']

    # Query Zenodo for a dataset linked with the publication's DOI (simple search using the publication's DOI)
    response = requests.get('https://zenodo.org/api/records',
                            params={'q': this_doi,
                                    'access_token': access_token})

    # status 400 means bad request
    if response.status_code == 400:
        print('400 bad request code, for search ' + this_doi)
    if response.status_code == 500:
            print('500 internal server issue, for search ' + this_doi)
    else:
        # Print results in the command window
        # print(response.json())

        # Load results in a python dict
        data = response.json()

        # Check if there was a hit (anything returned?). If there is 1 or more hit, load the data doi(s) in new variable
        data_dois = []
        if len(data["hits"]["hits"]) == 0:
            print('No dataset found by Zenodo for search ' + this_doi)
        else:
            print(str(len(data["hits"]["hits"])) + ' dataset(s) entry found in Zenodo for search ' + this_doi)
            for hit in data["hits"]["hits"]:
                data_dois.append(hit["doi"])
            is_dataset = 1

        data_dois_column.append(data_dois)
        is_dataset_column.append(is_dataset)

# Add dataset info to the master list (dataframe) and save as csv.

a = 0