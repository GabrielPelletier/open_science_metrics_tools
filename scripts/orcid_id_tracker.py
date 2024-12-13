# This script is meant to measure the number of Neuro researchers that have an ORCID ID
# Currently just in a test state to play around the ORCID API and learn how to use it.

import requests
import json
import os
import pandas as pd
from csv import writer

# Set directory and output file name
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = ROOT_DIR + '/data/ponctual_search_results/'
# Define data file name + Set path for output file
file_name = 'neuro_pis_orcid'
file_path = data_dir + file_name + '.csv'

# add HEADER to file
data_row = ['name_from_list', 'orcid_id', 'orcid_first_name', 'orcid_last_name', 'orcid_credit_name', 'orcid_other_name', 'orcid_email',
            'orcid_affiliation', 'is_orcid']
with open(file_path, 'a', newline='', encoding='utf-8') as f_object:
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(data_row)
    # Close the file object
    f_object.close()

# If you did not already generate a Token with your credentials to use the API, you need to do run the following lines
# first. Then save the token in your environment variables so you can load it before calling the API.

# orcid_auth_url = 'https://pub.orcid.org/oauth/token'
# data = {
#     "grant_type": 'client_credentials',
#     "client_id": 'REPLACE-by-Your-API-client-ID',
#     "client_secret": 'REPLACE-by-Your-API-secret',
#     "scope": '/read-public'
# }
# auth_response = requests.post(orcid_auth_url, data=data)
# auth_response_json = auth_response.json()
# auth_token = auth_response_json["access_token"]

# load my ORCID API Token from my Environment variables (Windows 10). Has to be set-up prior.
auth_token = os.environ.get('orcid_api_token')
auth_token_header_value = "Bearer %s" % auth_token

# Load Researchers list and loop through it.
pi_list = pd.read_csv(ROOT_DIR + '/data/queries_and_lists_for_ponctual_searches/neuro_author_list_2024.csv')

for row in pi_list.index:

    # get the name of the researcher
    first_name = pi_list['first_name'][row]
    last_name = pi_list['last_name'][row]
    full_name = first_name + ' ' + last_name

    # Prepare the API query for this researcher
    query = 'https://pub.orcid.org/v3.0/expanded-search/?q=' + \
            'given-names:' + first_name + '+AND+' + 'family-name:' + last_name

    headers = {'Content-type': 'application/vnd.orcid+json',
               'Authorization': auth_token_header_value}

    # Send the query, record the response and format the json output in something we can work with
    response = requests.get(query, headers=headers)
    data = response.json()
    data = data['expanded-result']
    dataframe = pd.DataFrame(data)

    # If 0 results were returned, save this information. If one or more results were found, continue on to check
    # affiliations
    if dataframe.empty:
        is_orcid = 0
        orcid_id = 'no orcid records found'
        orcid_first_name = 'none'
        orcid_last_name = 'none'
        orcid_credit_name = 'none'
        orcid_other_name = 'none'
        orcid_email = 'none'
        orcid_affiliation = 'none'
        # Write data to file
        data_row = [full_name, orcid_id, orcid_first_name, orcid_last_name, orcid_credit_name, orcid_other_name, orcid_email,
                    orcid_affiliation, is_orcid]
        with open(file_path, 'a', newline='', encoding='utf-8') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(data_row)
            # Close the file object
            f_object.close()
    else:
        is_orcid = 1
        for row in dataframe.index:
            orcid_id = dataframe['orcid-id'][row]
            orcid_first_name = dataframe['family-names'][row]
            orcid_last_name = dataframe['given-names'][row]
            orcid_credit_name = dataframe['credit-name'][row]
            orcid_other_name = dataframe['other-name'][row]
            orcid_email = dataframe['email'][row]
            orcid_affiliation = dataframe['institution-name'][row]
            # Write data to file
            data_row = [full_name, orcid_id, orcid_first_name, orcid_last_name, orcid_credit_name, orcid_other_name, orcid_email,
                        orcid_affiliation, is_orcid]
            with open(file_path, 'a', newline='', encoding='utf-8') as f_object:
                # Pass the CSV  file object to the writer() function
                writer_object = writer(f_object)
                # Result - a writer object
                # Pass the data in the list as an argument into the writerow() function
                writer_object.writerow(data_row)
                # Close the file object
                f_object.close()

