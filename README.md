# open_science_metrics_tools
Set of tools to track Open Science metrics at an institutional level.

# Contributors
* **Gabriel Pelletier**

  Open Science Data Manager, Tanenbaum Open Science Institute (TOSI) [gabriel.pelletier@mcgill.ca]

# Current set of tools
## Open Access (OA) Publishing Metrics
* **open_access_publication_tracker.py**

  This script is meant to be run regularly to update the list of publications by any author affiliated with the institution. Eventually will be set-up to run automatically once every few days or so using GitHub Actions.
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
