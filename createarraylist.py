import json
import os


def main():
    base_path = "assets/"
    dirs = os.listdir(base_path)
    for directory in dirs:
        names_list = list()
        for file in os.listdir(base_path + directory):
            if os.path.isfile(base_path + directory + f"/{file}"):
                names_list.append(file[:-4])
        print(f"{directory.upper()} : {json.dumps(names_list)} : {len(names_list)}")


if __name__ == '__main__':
    main()
