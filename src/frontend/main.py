import os
import json
from ..pcgcore.main import PCGCore

class FrontEnd():

    def __init__(self, db_name, dimensions):

        json_file_path = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(json_file_path, '../db/', db_name)
        with open(json_file_path) as json_file:
            self.db = json.load(json_file)

        self.dimensions = dimensions
        self.pcg = PCGCore(db_name, dimensions)

    def generate(self, y_offset_structures, x_offset_plane, y_offset_plane, z_offset_plane, ground_material):
        blocks = []

        # create ground
        for x in range(self.dimensions[0], (self.dimensions[1]+1)):
            for z in range(self.dimensions[2], (self.dimensions[3]+1)):
                blocks.append({
                        'x':x+x_offset_plane,
                        'y':0+y_offset_plane,
                        'z':z+z_offset_plane,
                        'material':ground_material
                    })

        structures = self.pcg.generate()


        plane_width = self.dimensions[1] - self.dimensions[0]
        plane_length = self.dimensions[3] - self.dimensions[2]
        # translate structures
        for structure in structures:
            for substruct in self.db[structure['name']]['structure']:
                for pos in substruct['position']:
                    blocks.append({
                            'x':pos[0]+structure['position'][0] + x_offset_plane - (plane_width//2),
                            'y':pos[1]+y_offset_structures,
                            'z':pos[2]+structure['position'][1] + z_offset_plane - (plane_length//2),
                            'material':substruct['material']
                        })        

        return blocks