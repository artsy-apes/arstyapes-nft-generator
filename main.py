import json
import os
import sys
import random
import pprint as pp

from PIL import Image


def select_image_attributes(attributes):
    image = dict()
    for att in attributes:
        image[att] = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]
        if att == "body":  # take the head with same color
            color = image[att].split("-")[0]
            image["head"] = f"{color}-head"
        if "zombie" in image[att]:  # Zombie head has custom eyes
            del image["eye"]
        if "squidgame" in image[att]:  # Squidgame ape has only background and outfit
            for trait in list(image):
                if trait in ["background", "outfit"]:
                    continue
                del image[trait]
        if "gasmask" in image[att]:  # Remove jewrely, mouth trait and eyes
            for trait in list(image):
                if trait in ["jewrely", "mouth attributes", "eyes"]:
                    del image[trait]
        # if "astronaut" in image[att]:
        #     del image["headwear"]
        #     image["astronaut_background"] = "astronaut 2"

    return image


def generate_ape_image(id_num: int, image: dict):
    traits_render_order = ["background", "body", "outfit", "head", "eye", "jewrely", "mouth attributes", "accessories",
                           "headwear"]
    ape = None
    for trait in traits_render_order:
        try:
            trait_img = Image.open(f'assets/{trait}/{image[trait]}.png').convert('RGBA')
            if ape is None:
                ape = trait_img
            else:
                ape = Image.alpha_composite(ape, trait_img)
        except KeyError:
            continue

    rgb = ape.convert('RGBA')
    file_name = str("artsyape-" + str(id_num)) + '.png'

    if not os.path.exists("generated"):
        os.mkdir('generated')
    rgb.save("./generated/" + file_name, optimize=True, quality=20)

    # Count how many apes generated
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} ape generated.".format(id_num))
    sys.stdout.flush()


def generate_special_ape_image(special_type: str):
    print(special_type)


def main():
    with open('config.json') as f:
        config = json.load(f)

    images = list()
    it = 0
    while it < config['total_images']:
        image = select_image_attributes(config['attributes'])
        if image not in images:
            images.append(image)
            it += 1

    for i in range(len(images)):
        generate_ape_image(i, images[i])

    # generate_images(images)


if __name__ == '__main__':
    main()
