# Figures for one-year (or some other time frame)
# summary information about Publications numbers and Open Access Status
# Gabriel Pelletier, June 2022

# Import modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = ROOT_DIR + '/data/ponctual_search_results/'
file = 'y2021_oa_info_cleaned.csv'
year_df = pd.read_csv(data_dir + file)

# Get Sum and Ratio of OA papers and by OA type
num_pub = len(year_df)
sum_is_oa = sum(year_df['is_open_access'] == True)
sum_closed = len(year_df) - sum_is_oa
ratio_is_oa = sum(year_df['is_open_access'] == True) / len(year_df)
sum_green_oa = sum(year_df['oa_type'] == 'green')
ratio_green_oa = sum(year_df['oa_type'] == 'green') / sum(year_df['is_open_access'] == True)
sum_gold_oa = sum(year_df['oa_type'] == 'gold')
ratio_gold_oa = sum(year_df['oa_type'] == 'gold') / sum(year_df['is_open_access'] == True)
sum_bronze_oa = sum(year_df['oa_type'] == 'bronze')
ratio_bronze_oa = sum(year_df['oa_type'] == 'bronze') / sum(year_df['is_open_access'] == True)
sum_hybrid_oa = sum(year_df['oa_type'] == 'hybrid')
ratio_hybrid_oa = sum(year_df['oa_type'] == 'hybrid') / sum(year_df['is_open_access'] == True)

# Extra analysis about Green OA as PrePrint vs Repository
sum_green_preprint = sum((year_df['oa_type'] == 'green') & (year_df['oa_version'] == 'submittedVersion'))
sum_green_repo = sum_green_oa - sum_green_preprint
ratio_green_preprint = sum_green_preprint / sum_is_oa
ratio_green_repo = sum_green_repo / sum_is_oa

# Print output in terminal
print('Num of publications: ' + str(num_pub))
print('Num OA: ' + str(sum_is_oa))
print('Num closed: ' + str(num_pub - sum_is_oa))
print('Num Gold: ' + str(sum_gold_oa))
print('Num Green: ' + str(sum_green_oa))
print('Num Bronze: ' + str(sum_bronze_oa))
print('Num Hybrid: ' + str(sum_hybrid_oa))
print('Num Green & Preprint: ' + str(sum_green_preprint))
print('Num Green & Reposiroty: ' + str(sum_green_repo))

# Plot Open vs Closed
data = np.array([sum_is_oa, sum_closed])
mylabels = ["Open Access", "Closed"]
myexplode = [0.2, 0]
mycolors = ["DarkOrange", "DimGray"]
textprops = {"fontsize": 14}

patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=mylabels, explode=myexplode, colors=mycolors,
                                    textprops=textprops)
# Add raw numbers as text manually placed on the pie chart (NOT IDEAL)
plt.text(-0.55, 0.45, '(n= ' + str(sum_is_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(0.4, -0.6, '(n= ' + str(sum_closed) + ')', horizontalalignment='center',
     verticalalignment='center')

[_.set_fontsize(18) for _ in texts]
plt.show()

# Plot Types of OA
data = np.array([ratio_gold_oa, ratio_bronze_oa, ratio_green_preprint, ratio_green_repo, ratio_hybrid_oa])
mylabels = ["Gold", "Bronze", "Green-Prep", "Green-Repo", "Hybrid"]
myexplode = [0.1, 0.1, 0.1, 0.1, 0.1]
textprops = {"fontsize": 14}
mycolors = ["DarkOrange", "SaddleBrown", "Green", "DarkGreen", "Silver"]
patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=mylabels, explode=myexplode, colors=mycolors,
                                    textprops=textprops, startangle=315)
# Add raw numbers as text manually placed on the pie chart (NOT IDEAL)
plt.text(1.2, 0.72, '(n= ' + str(sum_gold_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(0.5, -1.35, '(n= ' + str(sum_hybrid_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(-1.26, -0.7, '(n= ' + str(sum_green_repo) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(-1.38, -0.07, '(n= ' + str(sum_green_preprint) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(-1.25, 0.42, '(n= ' + str(sum_bronze_oa) + ')', horizontalalignment='center',
     verticalalignment='center')

[_.set_fontsize(18) for _ in texts]
plt.show()


a = 0