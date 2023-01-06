# This script calculates the OA numbers from each year's raw OA output and plots the trend across time.
# Gabriel Pelletier, June 2022

# Import modules
import pandas as pd
import matplotlib.pyplot as plt
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# *=*=* *=*=* First, Agregate OA numbers from raw file(s) containing every paper for that year *=*=* *=*=*
data_dir = ROOT_DIR + '/data/ponctual_search_results/'
# Define a file list (to be loaded) and corresponding year (for plotting)
#file_list = ['aff_oa_info_2010', 'aff_oa_info_2011', 'aff_oa_info_2012', 'aff_oa_info_2013', 'aff_oa_info_2014', 'aff_oa_info_2015',
#             'aff_oa_info_2016', 'aff_oa_info_2017', 'aff_oa_info_2018', 'aff_oa_info_2019', 'aff_oa_info_2020', 'aff_oa_info_2021']
file_list = ['y2010_oa_info', 'y2011_oa_info', 'y2012_oa_info', 'y2013_oa_info', 'y2014_oa_info', 'y2015_oa_info',
             'y2016_oa_info', 'y2017_oa_info', 'y2018_oa_info', 'y2019_oa_info', 'y2020_oa_info', 'y2021_oa_info', 'y2022_oa_info']
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
# Declare summar ydata lists that we will fill with yearly summary data
sum_publications_by_year = []
sum_is_oa_by_year = []
sum_closed_by_year = []
ratio_is_oa_by_year = []
ratio_closed_by_year = []
sum_green_oa_by_year = []
ratio_green_oa_by_year = []
sum_gold_oa_by_year = []
ratio_gold_oa_by_year = []
sum_bronze_oa_by_year = []
ratio_bronze_oa_by_year = []
sum_hybrid_oa_by_year = []
ratio_hybrid_oa_by_year = []
# Loop over file_list, calculate stuff and load in summary data lists
for file in file_list:
    # Load the file
    year_df = pd.read_csv(data_dir + file + '.csv')
    # Sum and Ratio of OA papers and by OA type
    sum_publications_by_year.append(len(year_df))
    sum_is_oa_by_year.append(sum(year_df['is_oa'] == True))
    ratio_is_oa_by_year.append(sum(year_df['is_oa'] == True) / len(year_df))
    sum_closed_by_year.append(sum(year_df['is_oa'] == False))
    ratio_closed_by_year.append(sum(year_df['is_oa'] == False) / len(year_df))
    sum_green_oa_by_year.append(sum(year_df['oa_status'] == 'green'))
    ratio_green_oa_by_year.append(sum(year_df['oa_status'] == 'green') / sum(year_df['is_oa'] == True))
    sum_gold_oa_by_year.append(sum(year_df['oa_status'] == 'gold'))
    ratio_gold_oa_by_year.append(sum(year_df['oa_status'] == 'gold') / sum(year_df['is_oa'] == True))
    sum_bronze_oa_by_year.append(sum(year_df['oa_status'] == 'bronze'))
    ratio_bronze_oa_by_year.append(sum(year_df['oa_status'] == 'bronze') / sum(year_df['is_oa'] == True))
    sum_hybrid_oa_by_year.append(sum(year_df['oa_status'] == 'hybrid'))
    ratio_hybrid_oa_by_year.append(sum(year_df['oa_status'] == 'hybrid') / sum(year_df['is_oa'] == True))
# Combine the create summary data list into a single data frame
oa_by_year = pd.DataFrame(
    {'yearly_report_file': file_list,
     'year': years,
     'num_publications': sum_publications_by_year,
     'sum_closed': sum_closed_by_year,
     'ratio_closed': ratio_closed_by_year,
     'sum_oa': sum_is_oa_by_year,
     'ratio_oa': ratio_is_oa_by_year,
     'sum_green': sum_green_oa_by_year,
     'ratio_green': ratio_green_oa_by_year,
     'sum_gold': sum_gold_oa_by_year,
     'ratio_gold': ratio_gold_oa_by_year,
     'sum_bronze': sum_bronze_oa_by_year,
     'ratio_bronze': ratio_bronze_oa_by_year,
     'sum_hybrid': sum_hybrid_oa_by_year,
     'ratio_hybrid': ratio_hybrid_oa_by_year
     })
# Save summary data-frame as CSV
oa_by_year.to_csv(data_dir + 'summary_trends.csv')

# *=*=* *=*=* Secondly, Plot data *=*=* *=*=*

plt.rcParams.update({'font.size': 12})
# This plot is a line plot with the trend for OA vs non-OA (PERCENT publication)
plt.figure()
x = years
plt.plot(x, oa_by_year['ratio_oa']*100, color=(1, 0.73, 0.06), label='Open Access', linewidth=3)
plt.scatter(x, oa_by_year['ratio_oa']*100, color=(1, 0.73, 0.06), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['ratio_closed']*100, color='k', label='Closed', linewidth=3)
plt.scatter(x, oa_by_year['ratio_closed']*100, color='k', label='_nolegend_', linewidth=3)
plt.title("Percent of OA publications at The Neuro by year\n(PubMed search based on 109 Neuro PIs)")
plt.xlabel("Year")
plt.ylabel("Percent of publications")
plt.legend(loc="upper left")
plt.ylim([0, 100])
plt.tight_layout()
plt.show()

# This plot is a line plot with the trend for OA vs non-OA (NUMBER publications)
plt.figure()
x = years
plt.plot(x, oa_by_year['sum_oa'], color=(1, 0.73, 0.06), label='Open Access', linewidth=3)
plt.scatter(x, oa_by_year['sum_oa'], color=(1, 0.73, 0.06), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_closed'], color='k', label='Closed', linewidth=3)
plt.scatter(x, oa_by_year['sum_closed'], color='k', label='_nolegend_', linewidth=3)
plt.title("Number of OA publications at The Neuro by year\n(PubMed search based on 109 Neuro PIs)")
plt.xlabel("Year")
plt.ylabel("Number of publications")
plt.legend(loc="upper left")
plt.ylim([0, 550])
plt.tight_layout()
plt.show()


# This plot is a line plot with the trend for each OA type (PERCENT BY YEAR)
plt.figure()
x = years

plt.plot(x, oa_by_year['ratio_gold']*100, color=(1, 0.73, 0.06), label='Gold', linewidth=3, )
plt.scatter(x, oa_by_year['ratio_gold']*100, color=(1, 0.73, 0.06), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['ratio_green']*100, color=(0.13, 0.82, 0.12), label='Green', linewidth=3)
plt.scatter(x, oa_by_year['ratio_green']*100, color=(0.13, 0.82, 0.12), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['ratio_bronze']*100, color=(0.57, 0.47, 0.13), label='Bronze', linewidth=3)
plt.scatter(x, oa_by_year['ratio_bronze']*100, color=(0.57, 0.47, 0.13), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['ratio_hybrid']*100, color=(0.68, 0.67, 0.61), label='Hybrid', linewidth=3)
plt.scatter(x, oa_by_year['ratio_hybrid']*100, color=(0.68, 0.67, 0.61), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['ratio_hybrid']*100, color=(1, 0.73, 0.06), linestyle='dotted', linewidth=3)
plt.xlabel("Year")
plt.ylabel("Percent of OA publications\nfor each OA type")
plt.title("% of each OA type among OA publications\n(PubMed search based on 109 Neuro PIs)")
plt.legend(loc="upper center")
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

# This plot is a lie plot with the trend for each OA type (NUMBER BY YEAR)
plt.figure()
x = years
plt.plot(x, oa_by_year['sum_closed'], color=(0, 0, 0), label='Closed', linewidth=3)
plt.scatter(x, oa_by_year['sum_closed'], color=(0, 0, 0), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_gold'], color=(1, 0.73, 0.06), label='Gold', linewidth=3)
plt.scatter(x, oa_by_year['sum_gold'], color=(1, 0.73, 0.06), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_green'], color=(0.13, 0.82, 0.12), label='Green', linewidth=3)
plt.scatter(x, oa_by_year['sum_green'], color=(0.13, 0.82, 0.12), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_bronze'], color=(0.57, 0.47, 0.13), label='Bronze', linewidth=3)
plt.scatter(x, oa_by_year['sum_bronze'], color=(0.57, 0.47, 0.13), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_hybrid'], color=(0.68, 0.67, 0.61), label='Hybrid', linewidth=3)
plt.scatter(x, oa_by_year['sum_hybrid'], color=(0.68, 0.67, 0.61), label='_nolegend_', linewidth=3)
plt.plot(x, oa_by_year['sum_hybrid'], color=(1, 0.73, 0.06), linestyle='dotted', linewidth=3)
plt.xlabel("Year")
plt.ylabel("Number of publications")
plt.title("Number publications of each OA type\n(PubMed search based on 109 Neuro PIs)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
