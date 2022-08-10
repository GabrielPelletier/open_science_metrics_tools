# This script is meant to update the publication master list and update the OA status.
# * The OA status of a paper may change from the time it was published (e.g., added to an institutional repo some time
# after publication)
# * Also tries to deal with/fix paper titles with special characters.
# * This code is associated with the open_access_publication_tracker.py, but ran independently
#
# Gabriel Pelletier
# August 2022

# Import packages/modules
import os
import shutil
import csv
from csv import writer
from datetime import datetime
import pandas
from pandas import *
from unpywall import Unpywall
from unpywall.utils import UnpywallCredentials
# Custom tool/utils/functions
from utils import *

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

### SET PARAMETERS HERE
# Email for unpaywall authentification (you don't need to register or anything)
UnpywallCredentials('gabriel.pelletier@mcgill.ca')
# Set directory(ies)
data_dir = ROOT_DIR + '/data/'
# Define data file name + Set path for output file
master_file_name = 'master_list'
master_file_path = data_dir + master_file_name + '.csv'
#### SET PARAMETERS END

# Intro Message
print('Updating the publication master list with the Unpaywall API')

# Copy current master_list to data/archive with timestamp before modifying master_list
todays_date = datetime.today()
shutil.copyfile(master_file_path,
                data_dir + 'archive/' + todays_date.strftime("%Y_%m_%d") + '_' + master_file_name + '.csv')

# Load the "master_list" csv data file containing all previously added publications into a DataFrame
master_df = read_csv(master_file_path)
# master_df = master_df.reset_index()
all_dois = master_df['doi'].tolist()

# Once loaded as a dataframe, open the old master_list.csv, wipe the content (truncate) and add header.
f = open(master_file_path, "w+")
f.close()
data_row = ['neuro_author_s', 'title', 'journal', 'doi', 'pmid', 'date_not_actual', 'is_open_access', 'oa_type',
            'oa_version', 'url_to_oa_version']
with open(master_file_path, 'a', newline='', encoding='utf-8') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(data_row)
    f_object.close()

# Loop over the lines of the master_list DataFrame
for index, row in master_df.iterrows():
    my_doi = row['doi']
    my_neuro_author_s = row['neuro_author_s']
    my_pmid = row['pmid']

    # Grab the publication DOI, and check it's OA status with the Unpaywall API
    try:
        oa_info = Unpywall.doi(dois=[my_doi])
        # Prepare Data to be saved
        is_oa = oa_info.at[0, 'is_oa']
        oa_type = oa_info.at[0, 'oa_status']
        my_title = oa_info.at[0, 'title']
        my_journal = oa_info.at[0, 'journal_name']
        my_date_not_actual = oa_info.at[0, 'published_date']
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

    # Prepare data to be added to the new master_list
    data_row = [my_neuro_author_s, my_title, my_journal, my_doi, my_pmid, my_date_not_actual, is_oa, oa_type,
                oa_version, oa_url]

    # Add data row to ongoing CSV file
    with open(master_file_path, 'a', newline='', encoding='utf-8') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(data_row)
        # Close the file object
        f_object.close()

# Read the updated csv file as a dataframe, Sort by Publication Date and re-save as csv
master_df = read_csv(master_file_path)
master_df["date_not_actual"] = master_df["date_not_actual"].astype('string')
master_df["date_not_actual"] = pandas.to_datetime(master_df["date_not_actual"])
master_df = master_df.sort_values(by='date_not_actual', ascending=False)
master_df.to_csv(master_file_path, index=False)

# Write data in HTML format and in MD formats for webpage
#create_html_file(master_file_path)
out_dir = ROOT_DIR + '/_steps/'
create_md_files(master_file_path, out_dir)

