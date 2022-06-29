# Test script to write markdown file using python
import os
from datetime import datetime

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
# input file
csv_file = ROOT_DIR + '/data/test_list.csv'
filein = open(csv_file, "r")
data = filein.readlines()


for line in data[:]:
    row = line.split(",")

    # create separate output md file for each publication
    md_file_name = ROOT_DIR + '/data/test_md.md'
    fileout = open(md_file_name, "w")

    date_text = datetime.strptime(row[5], '%m/%d/%Y').strftime('%Y-%m-%d') + " 00:00:00 -0700"

    # Define text and formatting based on Open Access Status
    if row[7] == 'closed':
        oa_text = 'This article is not available in Open Access\n'
    elif row[7] == 'gold':
        oa_text = 'This publication is available in Open Access! (Gold OA)\n' + \
                  '[Access it freely here](' + row[9] + ')\n'
    elif row[7] == 'hybrid':
        oa_text = 'This publication is available in Open Access! (Hybrid OA)\n' + \
                  '[Access it freely here](' + row[9] + ')\n'
    elif row[7] == 'green':
        oa_text = 'This publication is available in Open Access! (Green OA)\n' + \
                  '[Access it freely here](' + row[9] + ')\n'

    my_md_file = "---\n"
    my_md_file += "title: " + row[1] + "\n"
    my_md_file += "date: " + date_text + "\n"
    my_md_file += "enddate:\n"
    my_md_file += "---\n"
    my_md_file += "\n"
    my_md_file += oa_text + "\n"

    fileout.writelines(my_md_file)
    fileout.close()

filein.close()
