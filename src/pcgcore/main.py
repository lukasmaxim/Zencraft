import os
import json
import random
from level import *


# Note this is a mock implementation of the actual PCGCore
class PCGCore:

    def __init__(self, db_name, dimensions):

        json_file_path = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(json_file_path, '../db/', db_name)
        with open(json_file_path) as json_file:
            self.db = json.load(json_file)

        self.dimensions = dimensions
    
    def generate(self):
        '''
        structures = []
        for _ in range(15):
            structures.append({
                'x': random.randint(self.dimensions[0], self.dimensions[1]),
                'y': random.randint(self.dimensions[2], self.dimensions[3]),
                'name': 'tori'
            })
        '''
        width = self.dimensions[1] - self.dimensions[0]
        height = self.dimensions[3] - self.dimensions[2]
        level = Level(width, height)
        print('Structures added')
        for struct in level.structures:
            print(struct)

        return level.structures
