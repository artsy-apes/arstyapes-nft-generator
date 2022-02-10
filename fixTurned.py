import json
import os


def main():
    base_path = "generated/metadata_old"
    base_path2 = "generated/metadata2"
    dirs = os.listdir(base_path)

    last = None
    for file in dirs:
        path = os.path.join(base_path, file)
        try:
            with open(path, 'rb') as f:
                meta_data: dict = json.load(f)
                for (trait_type, item) in meta_data["traits"].items():
                    if trait_type == "outfit" and "Studo" in item:
                        print(file)

                f.close()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()