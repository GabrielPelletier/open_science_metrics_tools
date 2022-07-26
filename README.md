# Open Science Metrics Tools

 ~ **Ongoing Work, no stable release yet** ~

Set of tools to track Open Science practices at an institutional level

The goal is to eventually have tools to track:
* Open Access Publications
* Open Datasets
* Open Code and Software
* Open Protocols

# Contributors
* **Gabriel Pelletier**

  Open Science Data Manager, Tanenbaum Open Science Institute (TOSI) [gabriel.pelletier@mcgill.ca]

# Current set of tools
## Open Access (OA) Publishing Metrics
* **open_access_publication_tracker.py**

  This script is meant to be run regularly to update the list of publications by any author affiliated with the institution. Eventually will be set-up to run automatically once every few days or so using GitHub Actions.
  
  A prototype of a publication feed with open-access info and links for The Neuro is available as a github web page here: https://gabrielpelletier.github.io/open_science_metrics_tools/
* **ponctual_search_tool.py**

  This script can be used for ponctual queries (e.g., getting publications and OA status for a given year, or given researcher). Script should be modified manually to customize the query.

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
