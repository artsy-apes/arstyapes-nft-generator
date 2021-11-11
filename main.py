import enum
import json
import os
import sys
import random
import pprint as pp
from collections import OrderedDict

from PIL import Image

from Ape import Ape, ZombieApe, SquidgameApe, GasmaskApe, AstronautApe


def select_ape_traits(attributes):
    special_ape = None
    special_apes = ["zombie", "squidgame", "gasmask", "astronaut"]

    traits = dict()
    for att in attributes:
        trait = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]
        traits[att] = trait
        if att == "body":  # take the head with same color
            color = traits[att].split("-")[0]
            traits["head"] = f"{color}-head"

        special_ape = list(s for s in special_apes if s in traits[att])

    ape = Ape(traits)
    if len(special_ape):
        if special_ape[0] == "zombie":
            ape = ZombieApe(traits)
        elif special_ape[0] == "squidgame":
            ape = SquidgameApe(traits)
        elif special_ape[0] == "gasmask":
            ape = GasmaskApe(traits)
        elif special_ape[0] == "astronaut":
            traits["body"] = "astronaut 2"
            ape = AstronautApe(traits)

    return ape


# def generate_ape_image(id_num: int, image: dict):
#     ape = None
#     for trait in image["render_order"]:
#         try:
#             trait_img = Image.open(f'assets/{trait}/{image["traits"][trait]}.png').convert('RGBA')
#             if ape is None:
#                 ape = trait_img
#             else:
#                 ape = Image.alpha_composite(ape, trait_img)
#         except KeyError as e:
#             continue
#
#     rgb = ape.convert('RGBA')
#     file_name = str("artsyape-" + str(id_num)) + '.png'
#
#     if not os.path.exists("generated"):
#         os.mkdir('generated')
#     rgb.save("./generated/" + file_name, optimize=True, quality=20)
#
#     generate_json_metadata(id_num, image["traits"])
#
#     # Count how many apes generated
#     sys.stdout.write("\r")
#     sys.stdout.write("{:2d} ape generated.".format(id_num))
#     sys.stdout.flush()


def generate_json_metadata(id_num, data):
    if not os.path.exists("generated/metadata"):
        os.mkdir('generated/metadata')
    with open(f"./generated/metadata/artsyape-{str(id_num)}.json", "w") as f:
        json.dump(data, f, indent=4)


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
        apes[i].render(i)


if __name__ == '__main__':
    main()
