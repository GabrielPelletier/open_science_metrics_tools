# Figures for one-year (or some other time frame)
# summary information about Publications numbers and Open Access Status
# Gabriel Pelletier, June 2022

# Import modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_dir = 'data/ponctual_search_results/'
file = 'y2021_oa_info.csv'
year_df = pd.read_csv(data_dir + file)
# Get Sum and Ratio of OA papers and by OA type
sum_is_oa = sum(year_df['is_oa'] == True)
sum_closed = len(year_df) - sum_is_oa
ratio_is_oa = sum(year_df['is_oa'] == True) / len(year_df)
sum_green_oa = sum(year_df['oa_status'] == 'green')
ratio_green_oa = sum(year_df['oa_status'] == 'green') / sum(year_df['is_oa'] == True)
sum_gold_oa = sum(year_df['oa_status'] == 'gold')
ratio_gold_oa = sum(year_df['oa_status'] == 'gold') / sum(year_df['is_oa'] == True)
sum_bronze_oa = sum(year_df['oa_status'] == 'bronze')
ratio_bronze_oa = sum(year_df['oa_status'] == 'bronze') / sum(year_df['is_oa'] == True)
sum_hybrid_oa = sum(year_df['oa_status'] == 'hybrid')
ratio_hybrid_oa = sum(year_df['oa_status'] == 'hybrid') / sum(year_df['is_oa'] == True)

# Plot Open vs Closed
data = np.array([sum_is_oa, sum_closed])
mylabels = ["Open Access", "Closed"]
myexplode = [0.2, 0]
mycolors = ["DarkOrange", "DimGray"]
textprops = {"fontsize": 14}

patches, texts, autotexts = plt.pie(data, autopct='%1.1f%%', labels=mylabels, explode=myexplode, colors=mycolors,
                                    textprops=textprops)
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
[_.set_fontsize(18) for _ in texts]
plt.show()


a = 0