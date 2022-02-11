import json
import os


def main():
    base_path = "generated/metadata"
    dirs = os.listdir(base_path)

    last = None
    for file in dirs:
        path = os.path.join(base_path, file)
        try:
            with open(path, 'r+') as f:
                meta_data: dict = json.load(f)
                for (trait_type, item) in meta_data["traits"].items():
                    if trait_type == "headwear" and "Luart" in item:
                        meta_data["traits"]["mouth"] = "Nothing"
                        f.seek(0)
                        f.write(json.dumps(meta_data, indent=4))
                        f.truncate()

                f.close()

        except Exception as e:
            print(e)
            print(file)


if __name__ == '__main__':
    main()