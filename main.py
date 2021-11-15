import json
import random
import sys
from collections import OrderedDict
from Ape import Ape, ZombieApe, SquidgameApe, GasmaskApe, AstronautApe


def select_ape_traits(attributes):
    special_traits = ["zombie", "squidgame", "gasmask", "astronaut"]
    ape_special_traits = []

    traits = dict()
    for att in attributes:
        trait = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]
        traits[att] = trait
        if att == "body":  # take the head with same color
            color = traits[att].split("-")[0]
            traits["head"] = f"{color}-head"

        special_trait = list(s for s in special_traits if s in traits[att])
        if len(special_trait):
            ape_special_traits.append(special_trait[0])

    ape = Ape(traits)
    if len(ape_special_traits):
        if "zombie" in ape_special_traits:
            ape = ZombieApe(traits)
        if "gasmask" in ape_special_traits:
            ape = GasmaskApe(traits)
        if "squidgame" in ape_special_traits:
            ape = SquidgameApe(traits)
        if "astronaut" in ape_special_traits:
            traits["body"] = "astronaut 2"
            ape = AstronautApe(traits)
    return ape


def main():
    with open('config.json') as f:
        config = json.load(f, object_pairs_hook=OrderedDict)

    apes = list()
    it = 0
    while it < config['total_images']:
        ape = select_ape_traits(config['attributes'])
        if ape not in apes:
            apes.append(ape)
            it += 1

    for i in range(len(apes)):
        apes[i].id = i
        apes[i].render()
        # Count how many apes generated
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} ape generated.".format(i))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
