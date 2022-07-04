# Some tools and utils for the oa_publication_tracker
# Gabriel Pelletier
# June 2022

from datetime import datetime

def create_html_table(csv_file):
    # Writes a CSV table into a (rough) formatted HTML TABLE
    # The function requires 1 argument: the input file name.
    # It expects a comma-separated input file to parse into an html table,
    # and assumes that the column headers are located in the first row.

    filein = open(csv_file, "r")
    html_file_name = csv_file[:-4] + '.html'
    fileout = open(html_file_name, "w")
    data = filein.readlines()

    table = "<table>\n"

    # Create the table's column headers
    header = data[0].split(",")
    table += "  <tr style=background-color:#00FFF2>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

    # Create the table's row data
    for line in data[1:]:
        row = line.split(",")
        table += "  <tr>\n"
        for column in row:
            table += "    <td style=max-width:400px>{0}</td>\n".format(column.strip())
        table += "  </tr>\n"

    table += "</table>"

    fileout.writelines(table)
    fileout.close()
    filein.close()

def create_html_file(csv_file):
    # Writes a CSV table into a formatted HTML file
    # The function requires 1 argument: the input file name.
    # It expects a comma-separated input file to parse into an html table,
    # and assumes that the column headers are located in the first row.

    filein = open(csv_file, "r")
    html_file_name = csv_file[:-4] + '.html'
    fileout = open(html_file_name, "w")
    data = filein.readlines()

    my_html_file = "<!DOCTYPE html>\n"
    my_html_file += "<html>\n"
    my_html_file += "<body>\n"

    my_html_file += "</br>\n"
    my_html_file += "<h1> Publication Feed and Open Access Enhancer </h1>\n"
    my_html_file += "<p>Up-to-date list of Publications from authors affiliated with Research Institution. " \
                    "For each publication, information is provided as to whether the paper is available openly, " \
                    "and provides the link to an OA version if any.<p>\n"
    my_html_file += "</br>\n"

    # CSV has a header
    header = data[0].split(",")
    for column in header:
        a = 0

    # Create an "entry" for each row in the CSV
    for line in data[1:]:
        row = line.split(",")
        # Define text and formatting based on Open Access Status
        if row[7] == 'closed':
            title_text = '<h3 style="color:silver">' + row[1] + '</h3>\n'
            date_text = '<p style="color:silver">&emsp;Publication Date: ' + row[5] + '</p>\n'
            oa_text = '<p style="color:silver">&emsp;This publication is not available in Open Access : ( </p>\n'
        elif row[7] == 'gold':
            title_text = '<h3>' + row[1] + '</h3>\n'
            date_text = '<p>&emsp;Publication Date: ' + row[5] + '</p>\n'
            oa_text = '<p><strong>&emsp;This publication is available in Open Access! <span style="color:darkorange">(Gold OA)</span></strong></p>\n<p>&emsp;<a href=' + \
                      row[9] + ' target="_blank">Access it freely here.</a></p>\n'
        elif row[7] == 'hybrid':
            title_text = '<h3>' + row[1] + '</h3>\n'
            date_text = '<p>&emsp;Publication Date: ' + row[5] + '</p>\n'
            oa_text = '<p><strong>&emsp;This publication is available in Open Access! <span style="color:grey">(Hybrid OA)</span></strong></p>\n<p>&emsp;<a href=' + \
                      row[9] + ' target="_blank">Access it freely here.</a></p>\n'
        elif row[7] == 'green':
            title_text = '<h3>' + row[1] + '</h3>\n'
            date_text = '<p>&emsp;Publication Date: ' + row[5] + '</p>\n'
            oa_text = '<p><strong>&emsp;This publication is available in Open Access! <span style="color:green">(Green OA)</span></strong></p>\n<p>&emsp;<a href=' + \
                      row[9] + ' target="_blank">Access it freely here.</a></p>\n'
        # Write to file
        my_html_file += title_text
        my_html_file += date_text
        my_html_file += oa_text

        my_html_file += "</br>\n"

    my_html_file += "<body>\n"
    my_html_file += "</html>"

    fileout.writelines(my_html_file)
    fileout.close()
    filein.close()


def create_md_files(csv_file, out_dir):
    # Parses the CSV list containing many publications, and creates one markdown doc (.md)
    # for each of them, in preparation for the website display in a neat timeline.

    # input file
    filein = open(csv_file, "r")
    data = filein.readlines()

    pub_num = 0

    for line in data[1:]:
        row = line.split(",")
        pub_num += 1
        # create separate output md file for each publication
        md_file_name = out_dir + 'pub_' + str(pub_num) + '.md'
        fileout = open(md_file_name, "w")
        try:
            date_text = datetime.strptime(row[5], '%m/%d/%Y').strftime('%Y-%m-%d') + " 00:00:00 -0700"
        except:
            date_text = row[5]
        oa_logo_link = '"https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Open_Access_logo_PLoS_transparent.svg/800px-Open_Access_logo_PLoS_transparent.svg.png"'
        green_oa_logo_link = '"https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Open_Access_logo_PLoS_white_green.svg/576px-Open_Access_logo_PLoS_white_green.svg.png"'
        closed_logo_link = '"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Closed_Access_logo_transparent.svg/1200px-Closed_Access_logo_transparent.svg.png"'
        # Define text and formatting based on Open Access Status
        if row[7] == 'closed':
            oa_text = '<img src=' + closed_logo_link + ' alt="drawing" width="25" align="left"/> &nbsp;&nbsp;&nbsp;This publication is not available in Open Access.\n\n'
        elif row[7] == 'gold':
            oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Gold OA)\n\n' + \
                      '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
        elif row[7] == 'hybrid':
            oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Hybrid OA)\n\n' + \
                      '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
        elif row[7] == 'green':
            oa_text = '<img src=' + green_oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Green OA)\n\n' + \
                      '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
        elif row[7] == 'bronze':
            oa_text = '<img src=' + oa_logo_link + ' alt="drawing" width="50" align="left"/> &nbsp;&nbsp;&nbsp;This publication is available in **Open Access**! (Bronze OA)\n\n' + \
                      '&nbsp;&nbsp;&nbsp;[Access it freely here](' + row[9] + ')\n'
        else:
            oa_text = 'The publication DOI could not be resolved by Unpaywall. It may or may not be available in Open Access.\n\n'

        my_md_file = "---\n"
        my_md_file += 'title: ' + '"' + row[1] + '"' + '\n'
        my_md_file += "date: " + date_text + "\n"
        my_md_file += "enddate:\n"
        my_md_file += "---\n"
        my_md_file += "\n"
        my_md_file += 'Published in: *' + row[2] + '*\n\n'
        my_md_file += 'DOI: [' + row[3] +'](https://doi.org/' + row[3] + ')\n\n'
        my_md_file += oa_text + "\n"

        fileout.writelines(my_md_file)
        fileout.close()

    filein.close()
