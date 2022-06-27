# This script calculates the OA numbers from each year's raw OA output and plots the trend across time.
# Gabriel Pelletier, June 2022

# Import modules
import pandas as pd
import matplotlib.pyplot as plt

# *=*=* *=*=* First, Agregate OA numbers from raw file(s) containing every paper for that year *=*=* *=*=*
data_dir = 'data/ponctual_search_results/'
# Define a file list (to be loaded) and corresponding year (for plotting)
file_list = ['y2010_oa_info', 'y2011_oa_info', 'y2012_oa_info', 'y2013_oa_info', 'y2014_oa_info', 'y2015_oa_info',
             'y2016_oa_info', 'y2017_oa_info', 'y2018_oa_info', 'y2019_oa_info', 'y2020_oa_info', 'y2021_oa_info']
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
# Declare summar ydata lists that we will fill with yearly summary data
sum_is_oa_by_year = []
ratio_is_oa_by_year = []
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
    sum_is_oa_by_year.append(sum(year_df['is_oa'] == True))
    ratio_is_oa_by_year.append(sum(year_df['is_oa'] == True) / len(year_df))
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
# This plot is a lie plot with the trend for OA vs non-OA
plt.figure()
x = years
plt.plot(x, oa_by_year['ratio_oa']*100, color='k', linewidth=3)
plt.scatter(x, oa_by_year['ratio_oa']*100, color='k')
plt.title("Percent of OA publications at The Neuro by year")
plt.xlabel("Year")
plt.ylabel("Ratio of OA publications\n(all OA types confounded)")
plt.ylim([40, 100])
plt.show()
# This plot is a lie plot with the trend for each OA type
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
plt.title("Breakdown of Open Access publications by type")
plt.legend(loc="upper center")
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
