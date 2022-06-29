# Tool script to querry Open Access information to Unpaywall of several papers starting from a list of
# DOIs of papers
#
# Gabriel Pelletier
# June 2022

# Import packages/modules (have to be Installed before-hand)
import shutil
from csv import writer
import pandas as pd
# unpywall interacts with Unpaywall API
from unpywall import Unpywall
from unpywall.utils import UnpywallCredentials
from pymed import PubMed
from datetime import datetime
import numpy as np
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Get today's date
todays_date = datetime.today()

### SET PARAMETERS HERE
# Are you providing a list of DOIs (=TRUE) or PMIDS (=FALSE)?
# Email for unpaywall authentification (you don't need to register or anything)
my_email = 'gabriel.pelletier@mcgill.ca'
UnpywallCredentials(my_email)
# Set directory(ies)
data_dir = ROOT_DIR + '/data/ponctual_search_results/'
# Define data file names + Set path for files (input and output)
list_file_name = 'y2021_pubmed_search'
list_file_path = data_dir + list_file_name + '.csv'
output_file_name = todays_date.strftime("%Y_%m_%d") + '_output'
output_file_path = data_dir + output_file_name + '.csv'

### SET PARAMATERS END

# Load list of IDs you want to process (DOIs or PMIDS)
id_list_df = pd.read_csv(list_file_path)

oa_info_list = []

# Run list through UNPAYWALL to retrieve OA information

# Run the first item in the list to create the data frame
for index, row in id_list_df.head(1).iterrows():
    my_doi = row['DOI']
    oa_info_list = Unpywall.doi(dois=[my_doi])

for index, row in id_list_df.iterrows():
    my_doi = row['DOI']
    try:
        oa_info = Unpywall.doi(dois=[my_doi])
        oa_info_list = pd.concat([oa_info_list, oa_info], axis=0)
    except:
        continue

oa_info_list.to_csv(output_file_path)
