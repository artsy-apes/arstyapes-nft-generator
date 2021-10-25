import json
import os
import random
import pprint as pp
from collections import OrderedDict

from PIL import Image


def select_image_attributes(attributes):
    image = OrderedDict()

    for att in attributes:
        image[att] = random.choices(attributes[att]['images'], attributes[att]['weights'])[0]

    return image


def generate_images(images: list):
    for i in range(len(images)):
        img = images[i]

        background = Image.open(f'assets/background/{img["background"]}.png').convert('RGBA')
        outfit = Image.open(f'assets/outfit/{img["outfit"]}.png').convert('RGBA')
        head = Image.open(f'./assets/head/{img["head"]}.png').convert('RGBA')
        eye = Image.open(f'./assets/eye/{img["eye"]}.png').convert('RGBA')
        headwear = Image.open(f'./assets/headwear/{img["headwear"]}.png').convert('RGBA')

        ape = Image.alpha_composite(background, outfit)
        ape = Image.alpha_composite(ape, head)
        ape = Image.alpha_composite(ape, eye)
        ape = Image.alpha_composite(ape, headwear)

        rgb = ape.convert('RGBA')
        file_name = str("artsyape-" + str(i)) + '.png'

        if not os.path.exists("generated"):
            os.mkdir('generated')
        rgb.save("./generated/" + file_name)


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
