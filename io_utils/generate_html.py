from bs4 import BeautifulSoup
from collections import defaultdict

from format import parse_file, group_by_group


def generate_html_page_by_group(data_dict, output_file="outputs/timetable_by_groups.html"):
    """
    Generates an HTML page containing tables for each group in the provided data dictionary.

    :param data_dict: Dictionary where keys are table titles and values are lists of dictionaries representing rows.
    :param output_file: Name of the output HTML file.
    """
    # Create a new BeautifulSoup object for the HTML document
    soup = BeautifulSoup("<html><head><title>Timetable by Groups</title></head><body></body></html>", "html.parser")
    body = soup.body

    # Add a title to the page
    body.append(soup.new_tag("h1"))
    body.h1.string = "Timetable by Groups"

    # Collect data by group
    grouped_data = defaultdict(list)
    for table_title, rows in data_dict.items():
        for row in rows:
            group = row.get("Group", "Unknown")
            grouped_data[group].append(row)

    # Generate a table for each group
    for group, rows in grouped_data.items():
        # Add the group title
        title_tag = soup.new_tag("h2")
        title_tag.string = f"Group: {group}"
        body.append(title_tag)

        # Create the table
        table_tag = soup.new_tag("table", border="1", cellspacing="0", cellpadding="5",
                                 style="border-collapse: collapse; width: 100%;")

        # Create the table header
        if rows:
            header_row = soup.new_tag("tr")
            for header in rows[0].keys():
                th = soup.new_tag("th", style="background-color: #f2f2f2; text-align: left;")
                th.string = header
                header_row.append(th)
            table_tag.append(header_row)

            # Add the table rows
            for row in rows:
                table_row = soup.new_tag("tr")
                for cell in row.values():
                    td = soup.new_tag("td")
                    td.string = str(cell)
                    table_row.append(td)
                table_tag.append(table_row)

        body.append(table_tag)

    # Write to the output HTML file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())


file_path = 'outputs/to_format.txt'
data = parse_file(file_path)
grouped_data = group_by_group(data)
generate_html_page_by_group(grouped_data, "outputs/formatted_timetable.html")
