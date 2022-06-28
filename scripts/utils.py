# Some tools and utils for the oa_publication_tracker
# Gabriel Pelletier
# June 2022

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
