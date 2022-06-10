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

UnpywallCredentials('gabriel.pelletier@mcgill.ca')

if __name__ == '__main__':

    # Get today's date
    todays_date = datetime.today()

    # Set directory(ies)
    data_dir = 'data/'

    # Define filenames
    output_file_name = todays_date.strftime("%Y%m%d%H%M%S") + '_lit_search'
    output_file_path = data_dir + output_file_name + '.csv'

    # Print Header in output CSV file
    header = ['neuro_author_s', 'title', 'journal', 'doi', 'pmid', 'date_not_actual', 'is_open_access', 'oa_type',
                    'oa_version', 'url_to_oa_version']
    with open(output_file_path, 'a', newline='', encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(header)
        f_object.close()

    # Intro Message
    print('Running OA tracker using the PubMed API and Unpaywall API')

    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="oa_publication_tracker", email="gabriel.pelletier@mcgill.ca")

    # Set Affiliations: may use more than one possibilities to cover all variations
    affiliation_1 = '*montreal*neurological*'
    affiliation_2 = '*neurology*neurosurgery*'
    affiliation_3 = '*mcgill*'

    # Set Date Range for query
    date_from = '"2021/01/01"'
    date_to = '"2021/12/31"'

    # Create a GraphQL query in plain text (Concatenate criteria in a single query)
    # query = '(' + author_name + '[Author]) AND ((' + affiliation_1 + '[Affiliation]) OR (' + affiliation_2 + '[Affiliation]))'
    query = '(' + affiliation_1 + '[Affiliation]) OR ((' + affiliation_2 + '[Affiliation]) AND (' + affiliation_3 + '[Affiliation])) AND((' + date_from + '[Date - Publication] : ' + date_to + '[Date - Publication]))'
    print(f'PubMed Query: {query}')

    # Execute the query against the API
    results = pubmed.query(query, max_results=10000)

    # Loop over the retrieved articles
    for publication in results:
        # convert result for this publication into a python dictionary
        publication_dict = publication.toDict()
        # Print a JSON representation of the object
        #print(publication.toJSON())

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

        # Check OA status with the Unpaywall API based on the article's DOI
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

        my_journal =  publication_dict["journal"]
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
        with open(output_file_path, 'a', newline='', encoding='utf-8') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(data_row)
            # Close the file object
            f_object.close()

    # Write data in HTML format
    create_html_table(output_file_path)
