# This script is meant to measure the number of Neuro researchers that have an ORCID ID
# Currently just in a test state to play around the ORCID API and learn how to use it.

## INFO
# https://info.orcid.org/documentation/api-tutorials/api-tutorial-searching-the-orcid-registry/#easy-faq-2532
# https://developer.amazon.com/docs/app-submission-api/python-example.html

import requests
import json


# First, Get Token

# URL=https://sandbox.orcid.org/oauth/token
#   HEADER: Accept: application/json
#   METHOD: POST
#   DATA:
#     client_id=[Your public API client ID]
#     client_secret=[Your public API secret]
#     grant_type=client_credentials
#     scope=/read-public

# data = {
#     "grant_type": client_credentials,
#     "client_id": APP-XVCQJZRJJSP7B2KJ,
#     "client_secret": be821bba-0a03-4f4b-b572-6024a93fe1cd,
#     "scope": /read-public
# }



# Then Use token to call api with the query.
# response = requests.get('https://website.example/id', headers={'Authorization': 'access_token myToken'})


#https://pub.orcid.org/v3.0/expanded-search/?q=FIRSTNAME+AND+LASTNAME

# The following works directly from the browser without need for credentials.
#https://pub.orcid.org/v3.0/csv-search/?q=gabriel+AND+pelletier&fl=orcid,given-names,family-name,current-institution-affiliation-name




# Send the query and get the response/results
# THIS DOESNT WORK NEED AUTH TOKEN
query = 'https://pub.orcid.org/v3.0/csv-search/?q=gabriel+AND+pelletier&fl=orcid,given-names,family-name,' \
        'current-institution-affiliation-name'

response = requests.get(query)

# Print results in the command window
print(response.json())

# Load results in a python dict
data = response.json()

a = 0