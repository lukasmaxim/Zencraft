import os
import json
import random
from level import *


class PCGCore:

    def __init__(self, db_name, dimensions):

        json_file_path = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(json_file_path, '../db/', db_name)
        with open(json_file_path) as json_file:
            self.db = json.load(json_file)

        self.dimensions = dimensions
    
    def generate(self):
        
        names = [
            'stone_formation_1',
            'stone_formation_2',
            'stone_formation_3',
            'stone_formation_4',
            'stone_horizontal_1_ratio_rule',
            'stone_horizontal_2_ratio_rule',
            'stone_horizontal_3_ratio_rule',
            'stone_vertical_1_ratio_rule',
            'stone_vertical_2_ratio_rule',

            'tree_green_1',
            'tree_green_2',
            'tree_pink_1',
            'tree_pink_2',

            'lake',
            'river',
            'waterfall',

            'tori',
            'pavillion',
            'house',
            'pagoda',

            'filler_1',
            'filler_2',
            'filler_3'
        ]

        structures = []

        x = (self.dimensions[1] - self.dimensions[0]) // 10
        y = (self.dimensions[3] - self.dimensions[2]) // 2
        for structure in names:
            x += 5
            structures.append({
                'position': [x, y],
                'name': structure
            })
            x += self.db[structure]['dimensions'][0]
        
        return structures
