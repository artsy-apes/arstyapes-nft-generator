import json
import random
import pprint as pp


def select_image_attributes(config, weights=None):
    image = dict()
    attributes = config['attributes']

    for att in attributes:
        image[att] = random.choices(attributes[att]["images"], attributes[att]['weights'], k=1);

    return image


def main():
    with open('config.json') as f:
        config = json.load(f)

    for _ in range(config["total_images"]):
        image = select_image_attributes(config)


if __name__ == '__main__':
    main()
