import enum
import json
import os
import sys
import random
import pprint as pp
from collections import OrderedDict

from PIL import Image


def select_image_attributes(attributes):
    image = dict()
    traits = dict()
    image["traits"] = traits
    image["specialty"] = None
    image["render_order"] = ["background", "body", "outfit",
                             "head", "eye", "jewrely",
                             "mouth attributes", "accessories", "headwear"]

    for att in attributes:
        trait = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]
        traits[att] = trait
        if att == "body":  # take the head with same color
            color = traits[att].split("-")[0]
            traits["head"] = f"{color}-head"
        if "zombie" in traits[att]:  # Zombie head has custom eyes
            image["specialty"] = "zombie"
        if "squidgame" in traits[att]:  # Squidgame ape has only background and outfit
            image["specialty"] = "squidgame"
        if "gasmask" in traits[att]:  # Remove jewrely, mouth trait and eyes
            image["specialty"] = "gasmask"
        if "astronaut" in traits[att]:
            image["specialty"] = "astronaut"

    if image["specialty"] == "zombie":
        del traits["eye"]
    elif image["specialty"] == "squidgame":
        for trait in list(traits):
            if trait in ["background", "outfit"]:
                continue
            del traits[trait]
    elif image["specialty"] == "gasmask":
        for trait in list(traits):
            if trait in ["jewrely", "mouth attributes", "eyes"]:
                del traits[trait]
    elif image["specialty"] == "astronaut":
        for trait in list(traits):
            if trait in ["jewrely", "mouth attributes", "headwear"]:
                del traits[trait]
        traits["body"] = "astronaut 2"
        image["render_order"].append(image["render_order"].pop(2))  # render outfit as last

    return image


def generate_ape_image(id_num: int, image: dict):
    ape = None
    for trait in image["render_order"]:
        try:
            trait_img = Image.open(f'assets/{trait}/{image["traits"][trait]}.png').convert('RGBA')
            if ape is None:
                ape = trait_img
            else:
                ape = Image.alpha_composite(ape, trait_img)
        except KeyError as e:
            continue

    rgb = ape.convert('RGBA')
    file_name = str("artsyape-" + str(id_num)) + '.png'

    if not os.path.exists("generated"):
        os.mkdir('generated')
    rgb.save("./generated/" + file_name, optimize=True, quality=20)

    generate_json_metadata(id_num, image["traits"])

    # Count how many apes generated
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} ape generated.".format(id_num))
    sys.stdout.flush()

def generate_json_metadata(id_num, data):
    if not os.path.exists("generated/metadata"):
        os.mkdir('generated/metadata')
    with open(f"./generated/metadata/artsyape-{str(id_num)}.json", "w") as f:
        json.dump(data, f, indent=4)



def main():
    with open('config.json') as f:
        config = json.load(f, object_pairs_hook=OrderedDict)

    images = list()
    it = 0
    while it < config['total_images']:
        image = select_image_attributes(config['attributes'])
        if image not in images:
            images.append(image)
            it += 1

    for i in range(len(images)):
        generate_ape_image(i, images[i])


if __name__ == '__main__':
    main()
