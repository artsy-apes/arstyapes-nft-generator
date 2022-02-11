# Python program to convert
# JSON file to CSV
import json
import csv
import os

# Opening JSON file and loading the data
# into the variable data

def main():
    with open('list_metadata.json') as json_file:
        apes = json.load(json_file)

    # now we will open a file for writing
    data_file = open('metadata.csv', 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    count = 0;
    for ape in apes:
        if count == 0:
            # Writing headers of CSV file
            header = ["Token ID", "Token Name", "File Name"]
            header.extend(list(ape["traits"].keys()))
            csv_writer.writerow(header)
            count += 1
        ape_id = ape["id"]
        values = [ape_id, f"ArtsyApe {ape_id}", f"artsyape-{ape_id}"]
        values.extend(list(ape["traits"].values()))
        csv_writer.writerow(values)

    data_file.close()


if __name__ == '__main__':
    main()