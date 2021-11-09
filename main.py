import json
import os
import sys
import random
import pprint as pp

from PIL import Image


def select_image_attributes(attributes):
    image = dict()
    is_gasmask = False
    is_squid_game = False
    is_zombie = False
    for att in attributes:
        image[att] = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]
        if att == "body":  # take the head with same color
            color = image[att].split("-")[0]
            image["head"] = f"{color}-head"
        if "zombie" in image[att]:  # Zombie head has custom eyes
            is_zombie = True
        if "squidgame" in image[att]:  # Squidgame ape has only background and outfit
            is_squid_game = True
        if "gasmask" in image[att]: # Remove jewrely, mouth trait and eyes
            is_gasmask = True

    if is_zombie:
        del image["eye"]

    if is_squid_game:
        for trait in list(image):
            if trait == "background" or trait == "outfit":
                continue
            del image[trait]

    if is_gasmask:
        for trait in list(image):
            if trait == "jewrely" or trait == "mouth attributes" or trait == "eye":
                del image[trait]

    return image


def generate_images(images: list):
    traits_render_order = ["background", "body", "outfit", "head", "eye", "jewrely", "mouth attributes", "accessories", "headwear"]
    for i in range(len(images)):
        ape = None
        for trait in traits_render_order:
            try:
                trait_img = Image.open(f'assets/{trait}/{images[i][trait]}.png').convert('RGBA')
                if ape is None:
                    ape = trait_img
                else:
                    ape = Image.alpha_composite(ape, trait_img)
            except Exception as e:
                print(e)

        rgb = ape.convert('RGBA')
        file_name = str("artsyape-" + str(i)) + '.png'

        if not os.path.exists("generated"):
            os.mkdir('generated')
        rgb.save("./generated/" + file_name, optimize=True, quality=20)

        # Count how many apes generated
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} ape generated.".format(i))
        sys.stdout.flush()


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

    generate_images(images)


if __name__ == '__main__':
    main()
