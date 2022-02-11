# Python program to convert
# JSON file to CSV
import json
import csv
import os


# Opening JSON file and loading the data
# into the variable data

def metaDataToList():
    base_path = "generated/metadata"
    dirs = os.listdir(base_path)

    ape_list = []
    for file in dirs:
        path = os.path.join(base_path, file)
        try:
            with open(path, 'rb') as f:
                meta_data: dict = json.load(f)
                ape_list.append(meta_data)

        except Exception as e:
            print(e)

    return ape_list

def main():
    apes = metaDataToList()

    # now we will open a file for writing
    data_file = open('metadata.csv', 'w')
    # create the csv writer object
    csv_writer = csv.writer(data_file)

    header = False
    for ape in apes:
        if not header:
            # Writing headers of CSV file
            header = ["Token ID", "Token Name", "File Name"]
            header.extend(list(ape["traits"].keys()))
            csv_writer.writerow(header)
            header = True
        ape_id = ape["id"]
        values = [ape_id, f"ArtsyApe {ape_id}", f"artsyape-{ape_id}.jpeg"]
        values.extend(list(ape["traits"].values()))
        csv_writer.writerow(values)

    data_file.close()


if __name__ == '__main__':
    main()
