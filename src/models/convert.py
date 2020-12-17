import nbtlib
import json
import os
import glob
from offset_lookup import offset_lookup

cwd = os.getcwd()

in_dir = cwd + '/src/models/nbt/'
out_dir = cwd + '/src/models/'

to_json = {}

for filename in os.listdir(in_dir):
    if not filename.endswith('.nbt'):
        continue

    structure_to_json = {
        "dimensions": [],
        "offset": None,
        "structure": []
    }

    with nbtlib.load(in_dir + filename) as nbtfile:
        root = nbtfile.root

        size = root.get('size')
        blocks = root.get('blocks')
        palette = root.get('palette')

        for i, material in enumerate(palette):
            structure_to_json["dimensions"] = [size[0], size[1], size[2]]
            structure_to_json["offset"] = offset_lookup.get(filename.split('.')[0], "not in lookup")
            material_string = str(material["Name"])

            if "Properties" in material:
                properties = material["Properties"]

                material_string += "["

                props = {}

                for prop in properties:

                    props[prop] = properties.get(prop)

                for prop in sorted(props):
                    value = props[prop]
                    material_string = material_string + prop + "=" + value + ","

                material_string = material_string[:-1]
                material_string += "]"

            structure_to_json["structure"].append(
                {"material": material_string, "position": []})

            for block in blocks:
                if block["state"] == i:
                    pos = block["pos"]
                    structure_to_json["structure"][i]["position"].append(
                        [int(pos[0]), int(pos[1]), int(pos[2])])

        to_json[filename.split('.')[0]] = structure_to_json

    with open(out_dir + "structures" + ".json", 'w') as outfile:
        outfile.write(json.dumps(to_json))
