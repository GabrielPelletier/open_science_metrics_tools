# main script of the open access publication tracker
# oa_publication_tracker
#
# Gabriel Pelletier
# June 2022

# Import packages/modules (have to be Installed before-hand)
import shutil
from csv import writer
# pymed interacts with the PubMed API
import pandas
from pymed import PubMed
# upywall interacts with Unpaywall API
from unpywall import Unpywall
from unpywall.utils import UnpywallCredentials
# Custom tool/utils/functions
from utils import *
from datetime import datetime
from datetime import timedelta
from pandas import *
import re

if __name__ == '__main__':

    ### SET PARAMETERS HERE

    # Email for unpaywall authentification (you don't need to register or anything)
    UnpywallCredentials('gabriel.pelletier@mcgill.ca')
    # Number of days back for the start-date of the Pubmed Search
    n_days_back = 20
    # Max number of results returned by the PubMed search
    n_max_results = 50
    # Set directory(ies)
    data_dir = 'data/'
    # Define data file name + Set path for output file
    master_file_name = 'master_list'
    master_file_path = data_dir + master_file_name + '.csv'

    #### SET PARAMETERS END

    # Get today's date
    todays_date = datetime.today()

    # Copy current master_list to data/archive with timestamp before modifying master_list
    shutil.copyfile(master_file_path, data_dir + 'archive/' + todays_date.strftime("%Y_%m_%d") + '_' + master_file_name + '.csv')

    # Intro Message
    print('Running OA tracker using the PubMed API and Unpaywall API')

    # Load the "master" csv data file containing all previously added publications
    master_df = read_csv(master_file_path)
    previous_dois = master_df['doi'].tolist()

    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="oa_publication_tracker", email="gabriel.pelletier@mcgill.ca")

    # Set Affiliations: may use more than one possibilities to cover all variations
    affiliation_1 = '*montreal*neurological*'
    affiliation_2 = '*neurology*neurosurgery*'
    affiliation_3 = '*mcgill*'

    # Set Date Range for query
    # Subtract a number of days from today's date (e.g. 10)
    date_from = todays_date - timedelta(n_days_back)
    # format the date in the pubmed way
    date_from = date_from.strftime('%d/%m/%Y')

    # upper range = 3000 for until Now
    date_to = '"3000"'

    # Create a GraphQL query in plain text (Concatenate criteria in a single query)
    # query = '(' + author_name + '[Author]) AND ((' + affiliation_1 + '[Affiliation]) OR (' + affiliation_2 + '[Affiliation]))'
    query = '(' + affiliation_1 + '[Affiliation]) OR ((' + affiliation_2 + '[Affiliation]) AND (' + affiliation_3 + '[Affiliation])) AND((' + date_from + '[Date - Create] : ' + date_to + '[Date - Create]))'
    print(f'PubMed Query: {query}')

    # Execute the query against the API
    results = pubmed.query(query, max_results=n_max_results)

    # Loop over the retrieved articles
    for publication in results:
        # convert result for this publication into a python dictionary
        publication_dict = publication.toDict()

        # Check if multiple DOIs and PMIDs were returned (sort of bug from pymed) and if so grab the first DOI-pmid.
        if "\n" in publication_dict["doi"]:
            split_dois = publication_dict["doi"].split('\n')
            my_doi = split_dois[0]
        else:
            my_doi = publication_dict["doi"]

        if "\n" in publication_dict["pubmed_id"]:
            split_pmids = publication_dict["pubmed_id"].split('\n')
            my_pmid = split_pmids[0]
        else:
            my_pmid = publication_dict["pubmed_id"]

        # Check if this DOI is in existing master file.
        # If NOT, add it and do the following bits. If YES, then skip.
        if my_doi in previous_dois:
            continue

        # Grab the publication DOI, and check it's OA status with the Unpaywall API
        try:
            oa_info = Unpywall.doi(dois=[my_doi])
            # Prepare Data to be saved
            is_oa = oa_info.at[0, 'is_oa']
            oa_type = oa_info.at[0, 'oa_status']
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

        # Check in there's a comma in the title and Journal name
        my_title = publication_dict["title"]
        if "," in my_title:
            my_title = my_title.replace(",", "[comma]")

        my_journal = publication_dict["journal"]
        if "," in my_journal:
            my_journal = my_journal.replace(",", "[comma]")

        # Retrieve affiliated authors
        neuro_ided_authors = []
        author_list = publication_dict["authors"]
        # loop through that author list. Search for some Affiliation Keywords using "re" package ( .+ = wildcard)
        for author in author_list:
            if (author["affiliation"] is None) or (author["lastname"] is None) or (author["firstname"] is None):
                continue
            elif (bool(re.search('.+eurology.+eurosurgery', author["affiliation"])) and bool(re.search('.+c.ill', author["affiliation"])) or bool(re.search('.+ontr.al.+eurological', author["affiliation"]))):
                neuro_ided_authors.append(author["firstname"] + ' ' + author["lastname"])

        # prepare data to be logged
        separator = "; "
        neuro_ided_authors = separator.join(neuro_ided_authors)

        data_row = [neuro_ided_authors, my_title, my_journal, my_doi, my_pmid,
                    publication_dict["publication_date"], is_oa, oa_type,
                    oa_version, oa_url]
        # doi_list.append(my_doi)
        # neuro_ided_author_list.append(author_name)
        # title_list.append(publication_dict["title"])
        # date_list.append(publication_dict["publication_date"])

        # Add data to ongoing CSV
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

    # Write data in HTML format
    create_html_table(master_file_path)
