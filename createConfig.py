import json
import os


def main():
    """
    Creates a config file from the assets folder.
    """
    config = {
        "total_images": 100,
        "traits": {}
    }
    attributes_types = ("background", "eye", "jewelry", "headwear", "mouth attributes", "body", "glasses", "outfit")

    base_path = "assets/"
    dirs = os.listdir(base_path)
    for directory in dirs:
        file_names = {}
        for file in os.listdir(base_path + directory):
            if os.path.isfile(base_path + directory + f"/{file}"):
                trait_name = file[:-4]
                if trait_name in ["Astronaut 2", "Orange Hoodie underlay", "Orange Hoodie overlay"]:
                    continue
                file_names[trait_name] = 10  # Add 10 as a default weight
        if directory in attributes_types:
            config["traits"][directory] = file_names

    with open("config.json", 'w+') as f:
        f.write(json.dumps(config, indent=4))
        f.close()


if __name__ == '__main__':
    main()
