import csv
import json
import os
import pandas as pd
from pprint import pprint


def calc_single_trait_percentage():
    csv_path = "metadata3777.csv"
    if not os.path.exists(csv_path):
        raise Exception("Generate collection first.")

    attributes_types = ("background", "ape", "eyes", "jewelry", "headwear", "mouth", "glasses", "outfit")

    count = {}
    for att in attributes_types:
        count[att] = {}

    csv_data = pd.read_csv(csv_path, index_col=False)
    csv_data.pop("Id")
    csv_data.pop("Token Name")
    csv_data.pop("File Name")
    csv_reader = csv.reader(csv_data.to_csv(index=None).split("\n"))

    header = []
    for row in csv_reader:
        if not len(header):
            header = row
            continue
        for it in range(len(row)):
            trait_type = header[it]
            trait = row[it]
            if trait in count[trait_type]:
                count[trait_type][trait] += 1
            else:
                count[trait_type].update({trait: 1})

    percentage = count.copy()
    for trait_type in percentage:
        for trait in percentage[trait_type]:
            percentage[trait_type][trait] = (percentage[trait_type][trait] / 3777) * 100

    return percentage

# def main():
#     """
#     Calculate how often does trait appear in the collection.
#     """
#     if not os.path.exists("metadata3777.csv"):
#         raise Exception("Generate collection first.")
#
#     attributes_types = ("background", "head", "eye", "jewelry", "headwear", "mouth attributes", "body", "glasses", "outfit")
#
#     base_path = "generated/metadata"
#     dirs = os.listdir(base_path)
#
#     count = {}
#     for att in attributes_types:
#         count[att] = {}
#
#     for file in dirs:
#         path = os.path.join(base_path, file)
#         with open(path, 'r') as f:
#             traits: dict = json.load(f)["traits"]
#             for (trait_type, item) in traits.items():
#                 if item in count[trait_type]:
#                     count[trait_type][item] += 1
#                 else:
#                     count[trait_type].update({item: 1})
#
#     percentage = count.copy()
#     for trait_type in percentage:
#         for trait in percentage[trait_type]:
#             percentage[trait_type][trait] = (percentage[trait_type][trait] / 3777) * 100
#
#     pprint(percentage)


if __name__ == '__main__':
    calc_single_trait_percentage()
