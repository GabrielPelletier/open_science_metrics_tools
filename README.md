# Open Science Metrics Tools

 ~ **Ongoing Work, no stable release yet** ~

Set of tools to track Open Science practices at an institutional level

The goal is to eventually have tools to track:
* Open Access Publications and Pre-Prints
* Open Datasets
* ORCID ID usage
* Open Code and Software
* Open Protocols

# Contributors
* **Gabriel Pelletier**

  Open Science Data Manager, Tanenbaum Open Science Institute (TOSI) [gabriel.pelletier@mcgill.ca]

# Current set of tools
## Open Access (OA) Publishing Metrics
* **open_access_publication_tracker.py**

  This script is meant to be run regularly to update the list of publications by any author affiliated with the institution. Eventually will be set-up to run automatically once every few days or so using GitHub Actions and CRON jobs.
  
  A prototype of a publication feed with open-access info and links for The Neuro is available as a github web page here: https://gabrielpelletier.github.io/open_science_metrics_tools/
    
    **Outputs:** One master CSV file : ROOT/data/master_list.csv which gets updated and added-to every time the tracker is run. In addition, one markdown (.md) file per publication gets created for visual display on the webpage, inside ROOT/_steps/
    
* **review_pub_oa_status.py**

    This script reviews and updates the entire master.csv list of all publications identified to date. It updates any changes to the publication information that might have occured after publication. Most importantly it updates the Open Access statuts of a publication which may change when the article is published in an instituional repository sometime after the publciaton because of an embargo period, for instance.
  
* **ponctual_search_tool.py**

  This script can be used for ponctual queries (e.g., getting publications and OA status for a given year, or given researcher). Script should be modified manually to customize the query.
  
 ## ORCID ID Usage Metrics
 * **orcid_id_tracker.py**
  
    This script takes a list of researchers (.csv format), queries whether they are any ORCID records matching each reseracher using the first-name and last-name using the ORCID public API, and outputs one .csv file containing all the matching ORCID IDs an affiliation information for all researchers, or a single row for reserachers without an ORCID, indicating no ORCID records were found.
  
    Manual verification is then needed to keep the ORCID records that match the reseracher, either looking at the affilation information or by seraching the ORCID ID in a search enginge trying to retrieve publications which link to the ID and assess whetehr the reseracher is the correct one associated with the institution of interest. This manual verification is not ideal, but is necessary because for researchers, not affiliation information is available on their public ORCID record.
  
    **Input:** One CSV file located in ROOT/data/queries_and_lists_for_ponctual_searches/ with the list of researchers, with one column for the last name (header 'last_name') and one column for the first name (header 'first_name'). The exact path filename is specified and can be modified at line 48.
  
    **Output:** One CSV file located in ROOT/data/ponctual_search_results/, currently named 'neuro_pis_orcid.csv'. The exact path filename is specified and can be modified at lines 12-15.
 
# Dependencies
* Python 3
## Python modules
  * pymed
  * unpywall
  * csv
  * pandas
  * datetime
  * re
  * requests
  * json
