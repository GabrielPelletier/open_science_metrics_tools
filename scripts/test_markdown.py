# Test script to write markdown file using python
import os
from datetime import datetime

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
# input file
csv_file = ROOT_DIR + '/data/test_list.csv'
filein = open(csv_file, "r")
data = filein.readlines()

pub_num = 0

for line in data[1:]:
    row = line.split(",")
    pub_num += 1
    # create separate output md file for each publication
    md_file_name = ROOT_DIR + '/_steps/pub_' + str(pub_num) + '.md'
    fileout = open(md_file_name, "w")
    date_text = datetime.strptime(row[5], '%m/%d/%Y').strftime('%Y-%m-%d') + " 00:00:00 -0700"
    oa_logo_link = '"https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Open_Access_logo_PLoS_transparent.svg/800px-Open_Access_logo_PLoS_transparent.svg.png"'
    # Define text and formatting based on Open Access Status
    if row[7] == 'closed':
        oa_text = 'This article is not available in Open Access\n\n'
    elif row[7] == 'gold':
        oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Gold OA)\n\n' + \
                  '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
    elif row[7] == 'hybrid':
        oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Hybrid OA)\n\n' + \
                  '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
    elif row[7] == 'green':
        oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Green OA)\n\n' + \
                  '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
    elif row[7] == 'bronze':
        oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Bronze OA)\n\n' + \
                  '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'

    my_md_file = "---\n"
    my_md_file += 'title: ' + '"' + row[1] + '"' + '\n'
    my_md_file += "date: " + date_text + "\n"
    my_md_file += "enddate:\n"
    my_md_file += "---\n"
    my_md_file += "\n"
    my_md_file += 'Published in: *' + row[2] + '*\n\n'
    my_md_file += 'DOI: ' + row[3] + '\n\n'
    my_md_file += oa_text + "\n"

    fileout.writelines(my_md_file)
    fileout.close()

filein.close()
