import json
import os
from copy import deepcopy
from PIL import Image


class Ape:
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "eye",
                    "mouth attributes", "glasses", "headwear"]

    def __init__(self, traits: dict):
        self._id = None
        self._traits = traits
        self.__traits_path = {}

        # Resolve traits path
        for _type, name in self.traits.items():
            path = f'assets/{_type}/{name}.png'

            if _type == "mouth attributes" and self._traits[_type] != "Respirator":
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'
            if _type == "jewlery" and self._traits[_type] == "Septum Piercing":
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'
            if _type == "headwear" and self.traits["head"] in ["Robin"] and self.traits["headwear"] in [
                "Gold crown", "Reverse hat", "Captains Hat"]:
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'
            if _type == "headwear" and self.traits["head"] in ["Juanita"] and self.traits["headwear"] in [
                "Gold crown", "Reverse hat"]:
                path = f'assets/{_type}/{self._traits["head"]}/{self._traits[_type]}.png'

            self.__traits_path[_type] = path

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

    def _has_face_jewelry(self) -> bool:
        face_jewelry = ["Cross earring", "Double Ear Piercing",
                        "Golden Earring (Left)", "Golden Eyebrow Piercing",
                        "Golden Nose Ring", "Septum Piercing"]
        return self.traits["jewelry"] in face_jewelry;

    def render(self):
        ape = None

        render_order = deepcopy(self.RENDER_ORDER)
        if self._has_face_jewelry() and type(self) is not GasmaskApe and type(self) is not AstronautApe:
            render_order[3], render_order[4] = render_order[4], render_order[3]

        for trait in render_order:
            try:
                trait_img = Image.open(self.__traits_path[trait]).convert('RGBA')
                ape = trait_img if (ape is None) else Image.alpha_composite(ape, trait_img)
            except KeyError as e:
                print(e)
                continue
            except Exception as e:
                print(e)
                print(self._traits)

        tag_img = Image.open("assets/tag/Tag white.png").convert('RGBA')
        ape = Image.alpha_composite(ape, tag_img)

        if not os.path.exists("generated"):
            os.mkdir('generated')

        ape = ape.convert('RGB')
        file_name = str("artsyape-" + str(self.id) + ".jpeg")
        ape.save("./generated/" + file_name, "JPEG", optimize=True, quality=30)

        self._create_json_metadata_file()

    def _create_json_metadata_file(self):
        if not os.path.exists("generated/metadata"):
            os.mkdir('generated/metadata')

        data = {
            "id": self.id,
            "traits": self._traits
        }
        with open(f"./generated/metadata/artsyape-{str(self.id)}.json", "w") as f:
            json.dump(data, f, indent=4)


class GoldenApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "mouth attributes",
                    "glasses", "headwear"]


class ZombieApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit",
                    "jewelry", "head", "mouth attributes",
                    "headwear"]


class AstronautApe(Ape):
    RENDER_ORDER = ["background", "body", "head",
                    "eye", "glasses", "outfit"]

    def __init__(self, traits: dict):
        if "Turned" in traits["head"]:
            traits["eye"] = "None"
        if "Golden" in traits["head"]:
            traits["eye"] = "None"
        if "Gasmask" in traits["glasses"]:
            traits["glasses"] = "None"
        super().__init__(traits)


class SquidgameApe(Ape):
    RENDER_ORDER = ["background", "outfit"]


class GasmaskApe(Ape):
    RENDER_ORDER = ["background", "body", "outfit", "head", "glasses", "headwear"]


class HoodieApe(Ape):
    def __init__(self, traits: dict):
        if "Turned" in traits["head"]:
            traits["eye"] = "None"
        if "Gasmask" in traits["glasses"]:
            traits["mouth attributes"] = "None"
        super().__init__(traits)
