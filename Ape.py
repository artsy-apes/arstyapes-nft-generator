import json
import os
import pprint

from PIL import Image


class Ape:
    RENDER_ORDER = ["background", "body", "outfit",
                    "head", "eye", "jewelry",
                    "mouth attributes", "accessories", "headwear"]

    def __init__(self, traits: dict):
        self._id = None
        self._traits = traits
        self._color = traits["head"].split("-")[0]

    def __eq__(self, other):
        return self._traits == other.traits

    @property
    def id(self):
        return self._id

    @property
    def traits(self):
        return self._traits

    @id.setter
    def id(self, id_num):
        self._id = id_num

    def render(self):
        ape = None
        for trait in self.RENDER_ORDER:
            try:
                trait_img = Image.open(f'assets/{trait}/{self._traits[trait]}.png').convert('RGBA')
                if trait == "mouth attributes" and self._traits[trait] != "mouthmask":
                    file_path = f'assets/{trait}/{self._color}/{self._traits[trait]}.png'
                    trait_img = Image.open(file_path).convert('RGBA')
                if ape is None:
                    ape = trait_img
                else:
                    ape = Image.alpha_composite(ape, trait_img)
            except KeyError:
                continue

        rgb = ape.convert('RGB')
        file_name = str("artsyape-" + str(self.id)) + '.png'

        if not os.path.exists("generated"):
            os.mkdir('generated')
        rgb.save("./generated/" + file_name, optimize=True, quality=20)

        self._generate_json_metadata()

    def _generate_json_metadata(self):
        if not os.path.exists("generated/metadata"):
            os.mkdir('generated/metadata')

        data = {
            "id": self.id,
            "traits": self._traits
        }
        with open(f"./generated/metadata/artsyape-{str(self.id)}.json", "w") as f:
            json.dump(data, f, indent=4)


class ZombieApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit",
                    "head", "jewelry", "mouth attributes",
                    "accessories", "headwear"]


class AstronautApe(Ape):
    RENDER_ORDER = ["background", "body", "head",
                    "eye", "accessories", "outfit"]

    def __init__(self, traits: dict):
        super().__init__(traits)
        if "zombie" in self._traits["body"]:
            self._traits["eye"] = "None"

        if "gasmask" in self._traits["accessories"]:
            self._traits["accessories"] = "None"


class SquidgameApe(Ape):
    RENDER_ORDER = ["background", "outfit"]


class GasmaskApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit", "head", "accessories", "headwear"]
