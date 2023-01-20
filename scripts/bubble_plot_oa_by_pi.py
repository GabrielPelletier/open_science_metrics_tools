import matplotlib.pyplot as plt
import pandas as pd

# read the CSV file
df = pd.read_csv('C:/Users/gpelle20/Desktop/open_science_metrics_tools/data/ponctual_search_results/20230117155545_oa_by_pi.csv')

# assign specific columns to list variables
x = df['dummy_rank'].tolist()
y = df['oa_ratio'].tolist()
z = df['n_papers'].tolist()
z_mod = [i * 8 for i in z]
threshold = df['dummy_threshold'].tolist()

plt.scatter(x, y, s=z_mod, alpha=0.3)
plt.title('OA Ratio by PI - Year 2022')
plt.xlabel('Individual PIs, ranked by OA Ratio')
plt.ylabel('Open Access Ratio (Threshold for "bonus" is 0.70)')

plt.axhline(y = 0.7, color = 'r', linestyle = '--')

plt.show()
