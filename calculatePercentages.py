import json
import os
from pprint import pprint


def main():
    """
    Calculate how often does trait appear in the collection.
    """
    if not os.path.exists("generated"):
        raise Exception("Generate collection first.")

    attributes_types = ("background", "head", "eye", "jewelry", "headwear", "mouth attributes", "body", "glasses", "outfit")

    base_path = "generated/metadata"
    dirs = os.listdir(base_path)

    count = {}
    for att in attributes_types:
        count[att] = {}

    for file in dirs:
        path = os.path.join(base_path, file)
        with open(path, 'r') as f:
            traits: dict = json.load(f)["traits"]
            for (trait_type, item) in traits.items():
                if item in count[trait_type]:
                    count[trait_type][item] += 1
                else:
                    count[trait_type].update({item: 1})

    percentage = count.copy()
    for trait_type in percentage:
        for trait in percentage[trait_type]:
            percentage[trait_type][trait] = (percentage[trait_type][trait] / 500) * 100

    pprint(percentage)





if __name__ == '__main__':
    main()
