import csv
import json
from copy import deepcopy
import os
import pandas as pd
from pprint import pprint


def open_metadata_csv():
    csv_path = "metadata3777.csv"

    csv_data = pd.read_csv(csv_path, index_col=False)
    csv_data.pop("Token Name")
    csv_data.pop("File Name")

    return csv.reader(csv_data.to_csv(index=None).split("\n"))


def save_to_cvs(path, header, csv_data):
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(csv_data)


def get_number_of_traits(id):
    apes_traits = open_metadata_csv()

    count = 0
    for ape in apes_traits:
        if len(ape) and ape[0] == str(id):
            ape.pop(0)
            for trait in ape:
                if trait != "None" and trait != "Nothing":
                    print(trait)
                    count += 1
    return count


def calc_single_trait_count_and_percentage():
    apes_traits = open_metadata_csv()

    attributes_types = ("background", "ape", "eyes", "jewelry", "headwear", "mouth", "glasses", "outfit")
    count = {}
    for att in attributes_types:
        count[att] = {}

    header = []
    for ape in apes_traits:
        if not len(header):
            header = ape
            continue
        for it in range(len(ape)):
            trait_type = header[it]
            trait = ape[it]
            if trait_type == "Id":
                continue
            if trait in count[trait_type]:
                count[trait_type][trait] += 1
            else:
                count[trait_type].update({trait: 1})

    percentage = deepcopy(count)
    for trait_type in percentage:
        for trait in percentage[trait_type]:
            percentage[trait_type][trait] = (percentage[trait_type][trait] / 3777)

    return count, percentage


def statistical_rarity(traits_percentage):
    apes_traits = open_metadata_csv()

    apes_statistical_rarity = []
    trait_types = []
    for ape in apes_traits:
        try:
            # Save header as trait types
            if not len(trait_types):
                trait_types = ape
                continue
            ape_rarity:float = 1.0
            trait_percentages = []
            for it in range(len(ape)):
                trait_type = trait_types[it]
                trait = ape[it]
                if trait_type == "Id":
                    continue
                else:
                    trait_percentages.append(traits_percentage[trait_type][trait])
                    ape_rarity *= traits_percentage[trait_type][trait]
            ape.extend(trait_percentages)
            # ape.append('{:.25f}'.format(ape_rarity))
            ape.append(ape_rarity)
            apes_statistical_rarity.append(ape)
        except Exception as e:
            continue

    trait_types.extend(['ape %', 'background %', 'eyes %', 'glasses %', 'jewelry %', 'headwear %', 'mouth %', 'outfit %'])
    save_to_cvs("statistical_rarity.csv", trait_types, apes_statistical_rarity)


def main():
    trait_count, traits_percentage = calc_single_trait_count_and_percentage()
    statistical_rarity(traits_percentage)


if __name__ == '__main__':
    print(get_number_of_traits(200))
