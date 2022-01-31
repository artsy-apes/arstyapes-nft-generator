import json
import random
import sys
from Ape import Ape, ZombieApe, SquidgameApe, GasmaskApe, AstronautApe, HoodieApe, GoldenApe


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
        ape_traits["body"] = "Astronaut 2"
        ape = AstronautApe(ape_traits)
    if "Orange Hoodie" in ape_traits["outfit"]:
        ape_traits["body"] = "Orange Hoodie underlay"
        ape_traits["headwear"] = "Orange Hoodie overlay"
        ape = HoodieApe(ape_traits)
    return ape


def main():
    with open('config.json') as f:
        config = json.load(f)

    apes = list()
    it = 0
    while it < config['total_images']:
        ape = select_ape_traits(config['traits'])
        if ape not in apes:
            apes.append(ape)
            it += 1

        sys.stdout.write("\r")
        sys.stdout.write("{:2d} ape generated.".format(it))
        sys.stdout.flush()

    for i in range(len(apes)):
        apes[i].id = i
        apes[i].render()
        # Count how many apes generated
        sys.stdout.write("\r")
        sys.stdout.write(f"{i} ape rendered.")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
