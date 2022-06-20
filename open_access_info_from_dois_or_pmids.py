# Tool script to querry Open Access information to Unpaywall of several papers starting from a list of
# DOIs of papers
#
# Gabriel Pelletier
# June 2022

# Import packages/modules (have to be Installed before-hand)
import shutil
from csv import writer
from pandas import *
# unpywall interacts with Unpaywall API
from unpywall import Unpywall
from unpywall.utils import UnpywallCredentials
from datetime import datetime


# Get today's date
todays_date = datetime.today()

### SET PARAMETERS HERE

# Email for unpaywall authentification (you don't need to register or anything)
UnpywallCredentials('gabriel.pelletier@mcgill.ca')
# Set directory(ies)
data_dir = 'data/ponctual_search_results/'
# Define data file names + Set path for files (input and output)
pmid_file_name = 'pmid_list'
pmid_file_path = data_dir + pmid_file_name + '.csv'
output_file_name = todays_date.strftime("%Y_%m_%d") + '_output'
output_file_path = data_dir + output_file_name + '.csv'

#### SET PARAMETERS END

# Load the pmid csv data file containing the pmid of publications for which you want OA info on
pmid_df = read_csv(pmid_file_path)

# Add Header to CSV
data_row = ['title', 'journal', 'doi', 'pmid', 'date_not_actual', 'is_open_access', 'oa_type', 'oa_version', 'oa_url']
with open(output_file_path, 'a', newline='', encoding='utf-8') as f_object:
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(data_row)
    # Close the file object
    f_object.close()

# Loop over the doi list
for index, row in pmid_df.iterrows():

    pmid = row['pmid']
    doi = row['doi']

    # Grab the publication DOI, and check it's OA status with the Unpaywall API
    try:
        oa_info = Unpywall.doi(dois=[doi])
        # Prepare Data to be saved
        is_oa = oa_info.at[0, 'is_oa']
        oa_type = oa_info.at[0, 'oa_status']
        title = oa_info.at[0, 'title']
        journal = oa_info.at[0, 'journal_name']
        date = oa_info.at[0, 'published_date']
        if oa_info.at[0, 'is_oa'] == True:
            oa_version = oa_info.at[0, 'best_oa_location.version']
            oa_url = oa_info.at[0, 'best_oa_location.url']
        elif oa_info.at[0, 'is_oa'] == False:
            oa_version = 'none'
            oa_url = 'none'
    except:
        # If DOI could not be resolved by Unpaywall
        is_oa = 'DOI not found by Unpaywall.'
        oa_type = ' '
        oa_version = ' '
        oa_url = ' '
        title = ' '

    #['title', 'journal', 'doi', 'pmid', 'date_not_actual', 'is_open_access', 'oa_type', 'oa_version', 'oa_url']
    data_row = [title, journal, doi, pmid, date, is_oa, oa_type, oa_version, oa_url]

    # Add data to ongoing CSV
    with open(output_file_path, 'a', newline='', encoding='utf-8') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(data_row)
        # Close the file object
        f_object.close()

