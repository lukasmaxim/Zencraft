import nbtlib
import json
import os
import glob
from offset_lookup import offset_lookup

cwd = os.getcwd()

in_dir = cwd + '/src/models/nbt/'
out_dir = cwd + '/src/models/json/'

for filename in os.listdir(in_dir):
    if not filename.endswith('.nbt'):
        continue

    to_json = {
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
            to_json["dimensions"] = [size[0], size[1], size[2]]
            to_json["offset"] = offset_lookup.get(filename.split('.')[0], "not in lookup")
            material_string = str(material["Name"])

            if "Properties" in material:
                properties = material["Properties"]

                material_string += "["

                for prop in properties:
                    value = material["Properties"].get(prop)

                    material_string = material_string + prop + "=" + value + ","

                material_string = material_string[:-1]
                material_string += "]"

            to_json["structure"].append(
                {"material": material_string, "position": []})

            for block in blocks:
                if block["state"] == i:
                    pos = block["pos"]
                    to_json["structure"][i]["position"].append(
                        [int(pos[0]), int(pos[1]), int(pos[2])])

        outname = filename.split('.')[0] + '.json'

        with open(out_dir + outname, 'w') as outfile:
            outfile.write(json.dumps(to_json))
