import json
import os
import random
import sys
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
    if "Gasmask" in ape_traits["glasses"]:
        ape = GasmaskApe(ape_traits)
    if "Squidgame" in ape_traits["outfit"]:
        ape = SquidgameApe(ape_traits)
    if "Astronaut" in ape_traits["outfit"]:
        ape = AstronautApe(ape_traits)
    if "Luart" in ape_traits["headwear"]:
        ape = LuartApe(ape_traits)
    if "Orange Hoodie" in ape_traits["outfit"]:
        ape = HoodieApe(ape_traits)
    return ape


def main():
    with open('config.json') as f:
        config = json.load(f)

    apes = list()

    # append predefined apes to the apes list
    predefined = ["captain", "space-brightsky", "chef",
                  "eggenberg", "golden", "lorent",
                  "beach", "space-gold","space-silver", "squid", "studo", "gostudent"]
    for dir in predefined:
        base_path = f"predefined/{dir}"
        for ape in os.listdir(base_path):
            file_name = os.path.join(base_path, ape)
            with open(file_name) as f:
                traits = json.load(f)
                ape = Ape(traits)
                if dir == "golden":
                    ape = GoldenApe(traits)
                if dir == "squid":
                    ape = SquidgameApe(traits)
                if "space" in dir:
                    ape = AstronautApe(traits)
                apes.append(ape)

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

    random.shuffle(apes)
    for i in range(len(apes)):
        apes[i].id = i + 1
        apes[i].render()
        # Count how many apes generated
        sys.stdout.write("\r")
        sys.stdout.write(f"{i} ape rendered.")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
