import json
import os
import random
import pprint as pp
from PIL import Image


def select_image_attributes(attributes):
    image = dict()

    for att in attributes:
        image[att] = random.choices(attributes[att]["images"], attributes[att]['weights'])[0]

    return image


def generate_images(images: list):
    for i in range(len(images)):
        img = images[i]

        body = Image.open(f'./assets/body/{img["body"]}.png').convert('RGBA')
        eyes = Image.open(f'./assets/eyes/{img["eyes"]}.png').convert('RGBA')
        mustache = Image.open(f'./assets/mustache/{img["mustache"]}.png').convert('RGBA')

        ape = Image.alpha_composite(body, eyes)
        ape = Image.alpha_composite(ape, mustache)

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
