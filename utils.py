# Some tools and utils for the oa_publication_tracker
# Gabriel Pelletier
# June 2022

def create_html_table(csv_file):
    # Writes a CSV table into a (rough) formatted HTML file
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
