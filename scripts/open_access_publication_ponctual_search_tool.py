# oa_publication_tracker
#
# This scrit is meant to run a ponctual search from pubmed and retrive the open access status of all papers returned from the serach.
# Search can either be done using a query in a text file, or by hard coding the query in this script.
#
# Gabriel Pelletier
# June 2022

# Import packages/modules (have to be Installed before-hand)
import shutil
from csv import writer
import csv
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
import os
import time

UnpywallCredentials('gabriel.pelletier@mcgill.ca')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    # Get today's date
    todays_date = datetime.today()
    # Intro Message
    print('Running OA tracker using the PubMed API and Unpaywall API')

    # Set directory(ies)
    data_dir = ROOT_DIR + '/data/ponctual_search_results/'
    # Define filenames
    output_file_name = todays_date.strftime("%Y%m%d%H%M%S") + '_lit_search'
    output_file_path = data_dir + output_file_name + '.csv'

    # SET QUERY
    # Several options.
    # 1. Query Composed of an AUTHOR name which is drawn from a list, and an AFFILIATION and DATE which are static
    # 2. Static query based only on AFFILIATION + DATE
    # query = '(' + affiliation_1 + '[Affiliation]) OR ((' + affiliation_2 + '[Affiliation]) AND (' + affiliation_3 + '[Affiliation])) AND((' + date_from + '[Date - Publication] : ' + date_to + '[Date - Publication]))'

    # First set the static portion of the query
    # Set Affiliations: may use more than one possibility to cover all variations
    #affiliation_1 = '*montreal*neurological*'
    #affiliation_2 = '*neurology*neurosurgery*'
    #affiliation_3 = '*mcgill*'
    # Set Date Range for query
    #date_from = '"2022/01/01"'
    #date_to = '"2022/12/31"'
    #base_query = '(' + affiliation_1 + '[Affiliation]) OR ((' + affiliation_2 + '[Affiliation]) AND (' + affiliation_3 + '[Affiliation])) AND((' + date_from + '[Date - Publication] : ' + date_to + '[Date - Publication]))'
    base_query = 'AND ("Montreal Neurological"[Affiliation] OR "McGill"[Affiliation]) AND 2023/01/01:2023/12/31[Date - Publication])'
    # Read QUERY, or AUTHOR LIST, from text file
    text_file = open(ROOT_DIR + "/data/queries_and_lists_for_ponctual_searches/neuro_author_list_2023.csv", "r", encoding='utf-8')
    author_list = list(csv.DictReader(text_file, delimiter=","))
    text_file.close()

    # Print Header in output CSV file
    header = ['neuro_author_s', 'title', 'journal', 'doi', 'pmid', 'date_not_actual', 'is_oa', 'oa_status',
                    'oa_version', 'url_to_oa_version']
    with open(output_file_path, 'a', newline='', encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(header)
        f_object.close()

    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="oa_publication_tracker", email="gabriel.pelletier@mail.mcgill.ca")

    # Loop author list
    for row in author_list:
        results = None
        # query in plain text for this author
        query = '(' + row["pubmed_author"] + '[Author] ' + base_query
        print(query)
        # Execute the query against the API
        results = pubmed.query(query, max_results=1000)
        time.sleep(2)
        # Loop over the retrieved articles
        for publication in results:
            # convert result for this publication into a python dictionary
            publication_dict = publication.toDict()
            # Print a JSON representation of the object
            #print(publication.toJSON())

            # If no DOI listed for this publication, skip it.
            if publication_dict["doi"] is None:
                continue

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

            try:
                my_journal = publication_dict["journal"]
                if "," in my_journal:
                    my_journal = my_journal.replace(",", "[comma]")
            except:
                continue

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


