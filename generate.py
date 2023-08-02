import json
import os
import random
import sys
import time

from Ape import Ape, ZombieApe, SquidgameApe, GasmaskApe, AstronautApe, HoodieApe, GoldenApe, LuartApe


def select_ape_traits(traits):
    ape_traits = dict()
    for trait_type, items in traits.items():
        trait_names = list(items.keys())
        weights = list(items.values())

        trait = random.choices(trait_names, weights)[0]
        ape_traits[trait_type] = trait
        if trait_type == "body":  # take the head with same color
            ape_traits["head"] = trait

    ape = Ape(ape_traits)
    if "Golden" in ape_traits["body"]:
        ape = GoldenApe(ape_traits)
    if "Turned" in ape_traits["body"]:
        ape = ZombieApe(ape_traits)
    if "Decontamination" in ape_traits["outfit"]:
        ape = SquidgameApe(ape_traits)
    if "Astronaut" in ape_traits["outfit"]:
        ape = AstronautApe(ape_traits)
    if "Orange Hoodie" in ape_traits["outfit"]:
        ape = HoodieApe(ape_traits)
    return ape


def generate():
    with open('configV2.json') as f:
        config = json.load(f)

    # list with all generated apes
    apes = list()

    # append predefined apes to the apes list
    # predefined = ["captain", "space-brightsky", "chef",
    #              "eggenberg", "golden", "lorent",
    #              "beach", "space-gold", "space-silver", "squid", "studo", "gostudent"]
    # for dir in predefined:
    #    base_path = f"predefined/{dir}"
    #    for ape in os.listdir(base_path):
    #        file_name = os.path.join(base_path, ape)
    #        with open(file_name) as f:
    #            traits = json.load(f)
    #            ape = Ape(traits)
    #            if dir == "golden":
    #                ape = GoldenApe(traits)
    #            if dir == "squid":
    #                ape = SquidgameApe(traits)
    #            if "space" in dir:
    #                ape = AstronautApe(traits)
    #            apes.append(ape)

    x = 548
    while x < 3778:
        print(x)
        generateById(x)
        x += 10000

    # generate and append random apes
    it = len(apes)
    while it < config['total_images']:
        ape = select_ape_traits(config['traits'])
        if ape not in apes:
            apes.append(ape)
            it += 1

            sys.stdout.write("\r")
            sys.stdout.write("{:2d} ape generated.".format(it))
            sys.stdout.flush()

    # start_time = time.time()
    random.shuffle(apes)
    for i in range(len(apes)):
        apes[i].id = i + 1
        apes[i].render()
        # Count how many apes generated
        sys.stdout.write("\r")
        sys.stdout.write(f"{i} Apes rendered.")
        # sys.stdout.write(f"{round(time.time() - start_time, 2)} seconds.")
        sys.stdout.flush()


def generateById(apeId: int):
    from rarity import open_metadata_csv
    meta_data_csv = open_metadata_csv()

    for row in meta_data_csv:
        if len(row) and row[0] == str(apeId):
            row.pop(0)
            traits = {
                "body": row[0],
                "head": row[0],
                "jewelry": row[4],
                "outfit": row[7],
                "eye": row[2],
                "mouth attributes": row[6],
                "background": row[1],
                "glasses": row[3],
                "headwear": row[5]
            }

            ape = Ape(traits)
            if "Golden" in traits["body"]:
                ape = GoldenApe(traits)
            if "Turned" in traits["body"]:
                ape = ZombieApe(traits)
            if "Decontamination" in traits["outfit"]:
                ape = SquidgameApe(traits)
            if "Astronaut" in traits["outfit"]:
                ape = AstronautApe(traits)
            if "Orange Hoodie" in traits["outfit"]:
                ape = HoodieApe(traits)
            ape.id = apeId
            ape.render()


if __name__ == '__main__':
    generate()
