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
file = 'y2021_oa_info_109.csv'
year_df = pd.read_csv(data_dir + file)
# Get Sum and Ratio of OA papers and by OA type
num_pub = len(year_df)
sum_is_oa = sum(year_df['is_open_access'] == 'TRUE')
sum_closed = len(year_df) - sum_is_oa
ratio_is_oa = sum(year_df['is_open_access'] == True) / len(year_df)
sum_green_oa = sum(year_df['oa_type'] == 'green')
ratio_green_oa = sum(year_df['oa_type'] == 'green') / sum(year_df['is_open_access'] == 'TRUE')
sum_gold_oa = sum(year_df['oa_type'] == 'gold')
ratio_gold_oa = sum(year_df['oa_type'] == 'gold') / sum(year_df['is_open_access'] == 'TRUE')
sum_bronze_oa = sum(year_df['oa_type'] == 'bronze')
ratio_bronze_oa = sum(year_df['oa_type'] == 'bronze') / sum(year_df['is_open_access'] == 'TRUE')
sum_hybrid_oa = sum(year_df['oa_type'] == 'hybrid')
ratio_hybrid_oa = sum(year_df['oa_type'] == 'hybrid') / sum(year_df['is_open_access'] == 'TRUE')
# Print output in terminal
print('Num of publications: ' + str(num_pub))
print('Num OA: ' + str(sum_is_oa))
print('Num closed: ' + str(num_pub - sum_is_oa))
print('Num Gold: ' + str(sum_gold_oa))
print('Num Green: ' + str(sum_green_oa))
print('Num Bronze: ' + str(sum_bronze_oa))
print('Num Hybrid: ' + str(sum_hybrid_oa))
# Plot Open vs Closed
data = np.array([sum_is_oa, sum_closed])
mylabels = ["Open Access", "Closed"]
myexplode = [0.2, 0]
mycolors = ["DarkOrange", "DimGray"]
textprops = {"fontsize": 14}

patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=mylabels, explode=myexplode, colors=mycolors,
                                    textprops=textprops)
# Add raw numbers as text manually placed on the pie chart (NOT IDEAL)
plt.text(-0.54, 0.47, '(' + str(sum_is_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(0.42, -0.57, '(' + str(sum_closed) + ')', horizontalalignment='center',
     verticalalignment='center')

[_.set_fontsize(18) for _ in texts]
plt.show()

# Plot Types of OA
data = np.array([ratio_gold_oa, ratio_bronze_oa, ratio_green_oa, ratio_hybrid_oa])
mylabels = ["Gold", "Bronze", "Green", "Hybrid"]
myexplode = [0.1, 0.1, 0.1, 0.1]
textprops = {"fontsize": 14}
mycolors = ["DarkOrange", "SaddleBrown", "Green", "Silver"]
patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=mylabels, explode=myexplode, colors=mycolors,
                                    textprops=textprops, startangle=315)
# Add raw numbers as text manually placed on the pie chart (NOT IDEAL)
plt.text(0.5, 0.38, '(' + str(sum_gold_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(0.02, -0.81, '(' + str(sum_hybrid_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(-0.68, -0.35, '(' + str(sum_green_oa) + ')', horizontalalignment='center',
     verticalalignment='center')
plt.text(-0.6, 0.22, '(' + str(sum_bronze_oa) + ')', horizontalalignment='center',
     verticalalignment='center')

[_.set_fontsize(18) for _ in texts]
plt.show()


a = 0