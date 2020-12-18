from cell import *
import random

STRUCTURE_KEYS = ['house', 'lake', 'pagoda', 'pavillion', 'river', 'stone_formation_1',
                  'stone_formation_2', 'stone_formation_3', 'stone_formation_4',
                  'tori', 'tree_green_1', 'tree_green_2', 'tree_pink_1', 'tree_pink_2', 
                  'stone_horizontal_1_ratio_rule',
                  'stone_horizontal_2_ratio_rule',
                  'stone_horizontal_3_ratio_rule',
                  'stone_vertical_1_ratio_rule',
                  'stone_vertical_2_ratio_rule',
                  'filler_1',
                  'filler_2',
                  'filler_3',
                  'waterfall'
                  ]

STRUCTURES = {
    'house': {'dim': [15, 11, 23], 'symbol':'H', 'rules':[]},
    'lake': {'dim': [19, 6, 18], 'symbol': '#', 'rules': [3]},
    'pagoda': {'dim': [13, 37, 16], 'symbol': 'A', 'rules': []},
    'pavillion': {'dim': [7, 9, 7], 'symbol': 'P', 'rules': []},
    'river': {'dim': [26, 6, 40], 'symbol': '~', 'rules': [5,6]},
    # 'stone_formation_1': {'dim': [11, 3, 10], 'symbol':'^', 'rules': [1,2]},
    # 'stone_formation_2': {'dim': [10, 3, 9], 'symbol': 'o', 'rules': [1,2]},
    # 'stone_formation_3': {'dim': [11, 3, 8], 'symbol': 'x', 'rules': [1,2]},
    # 'stone_formation_4': {'dim': [8, 2, 8], 'symbol': '@', 'rules': [1,2]},
    'stone_formation_1': {'dim': [9, 3, 8], 'symbol':'^', 'rules': [1,2]},
    'stone_formation_2': {'dim': [8, 3, 7], 'symbol': 'o', 'rules': [1,2]},
    'stone_formation_3': {'dim': [9, 3, 6], 'symbol': 'x', 'rules': [1,2]},
    'stone_formation_4': {'dim': [6, 2, 6], 'symbol': '@', 'rules': [1,2]},
    'tori': {'dim': [1, 5, 5], 'symbol': 'T', 'rules': []},
    'tree_green_1': {'dim': [8, 7, 6], 'symbol': 'TG1', 'rules': []},
    'tree_green_2': {'dim': [7, 9, 8], 'symbol': 'TG2', 'rules': []},
    'tree_pink_1': {'dim': [8, 12, 11], 'symbol': 'TP1', 'rules': [1,2]},
    'tree_pink_2': {'dim': [5, 6, 5], 'symbol': 'TP2', 'rules': [1,2]},
    'waterfall': {'dim': [16,11,19], 'symbol': 'W', 'rules': []},
    # 'stone_horizontal_1_ratio_rule': {'dim': [3,2,5], 'symbol': 'H1', 'rules': []},
    # 'stone_horizontal_2_ratio_rule': {'dim': [3,3,5], 'symbol': 'H2', 'rules': []},
    # 'stone_horizontal_3_ratio_rule': {'dim': [3,3,5], 'symbol': 'H3', 'rules': []},
    # 'stone_vertical_1_ratio_rule': {'dim': [4,4,4], 'symbol': 'V1', 'rules': []},
    # 'stone_vertical_2_ratio_rule': {'dim': [3,5,4], 'symbol': 'V2', 'rules': []},
    'filler_1': {'dim': [2,1,3], 'symbol': 'W', 'rules': []},
    'filler_2': {'dim': [3,1,5], 'symbol': 'W', 'rules': []},
    'filler_3': {'dim': [6,4,7], 'symbol': 'W', 'rules': []},
    'stone_horizontal_1_ratio_rule': {'dim': [1,2,3], 'symbol': 'H1', 'rules': []},
    'stone_horizontal_2_ratio_rule': {'dim': [1,3,3], 'symbol': 'H2', 'rules': []},
    'stone_horizontal_3_ratio_rule': {'dim': [1,3,3], 'symbol': 'H3', 'rules': []},
    'stone_vertical_1_ratio_rule': {'dim': [2,4,2], 'symbol': 'V1', 'rules': []},
    'stone_vertical_2_ratio_rule': {'dim': [1,5,2], 'symbol': 'V2', 'rules': []},
}

class Level(object):
    STRUCTURE_LIMIT = 5

    def __init__(self, width, height, structure_padding, max_no_buildings, max_no_nature, start=None):
        self.width, self.height, self.map, self.structures = width, height, {}, []
        self.structure_padding = structure_padding
        self.max_no_buildings = max_no_buildings
        self.max_no_nature = max_no_nature
        self.no_builindgs = 0
        self.no_nature = 0
        self.buildBlankLevel()
        self.placeStructures()
        
    def buildBlankLevel(self):
        self.map.update({ (i,j):Cell(i,j)
                            for i in range(self.width+2)
                            for j in range(self.height+2)
            })
        self.map.update({ (i,j):Wall(i,j)
                            for i in range(self.width+2)
                            for j in [0, self.height+1]
            })
        self.map.update({ (i,j):Wall(i,j)
                            for i in [0, self.width+1]
                            for j in range(self.height+2)
            })

    def placeStructures(self):
        x_cur = 1
        y_cur = 1
        while y_cur < self.height - 1:
            if  isinstance(self.map[(x_cur, y_cur)], Wall) or isinstance(self.map[(x_cur, y_cur)], Structure):
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1
            else:
                self.placeStructure(x_cur, y_cur)
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1

    def placeStructure(self, x_cur, y_cur):
        if (self.no_builindgs > self.max_no_buildings) and (self.no_nature > self.max_no_nature):
            return

        # Determine width
        #################
        # find available width
        x = x_cur
        while x < self.width:
            if isinstance(self.map[(x, y_cur)], Wall) or isinstance(self.map[(x, y_cur)], Structure):
                break
            x += 1
        available_width = x - x_cur

        # Determine height
        ##################

        y = y_cur
        while y < self.height:
            if isinstance(self.map[(x_cur, y)], Wall) or isinstance(self.map[(x_cur, y)], Structure):
                break
            y += 1
        available_height = y - y_cur

        # Find structure that fits in the available area
        trials = 0
        struct_key = random.choice(STRUCTURE_KEYS)
        struct_width = int(STRUCTURES[struct_key]['dim'][0]*self.structure_padding)
        struct_height = int(STRUCTURES[struct_key]['dim'][2]*self.structure_padding)
        struct_area = struct_width * struct_height
        while ((self.no_builindgs > self.max_no_buildings and self.isBuilindg(struct_key)) \
                and (self.no_nature > self.max_no_nature and self.isNature(struct_key)) \
                and (self.isAdded(struct_key) or struct_area > (available_width * available_height)) \
                and trials < 10):
            struct_key = random.choice(STRUCTURE_KEYS)
            #struct_width = int(STRUCTURES[struct_key]['dim'][0]*self.structure_padding)
            #struct_height = int(STRUCTURES[struct_key]['dim'][2]*self.structure_padding)
            struct_area = struct_width * struct_height
            trials += 1

        if self.isBuilindg(struct_key):
            self.no_builindgs += 1
        else:
            self.no_nature += 1

        if struct_area <= (available_width * available_height) and not self.isAdded(struct_key):
            print('Adding %s which fits in the available area at: (%s, %s)' % (struct_key, x_cur, y_cur))
            # Add structure to level
            ###################
            # add structure
            self.map.update({ (i,j):Structure(i,j, STRUCTURES[struct_key]['symbol'])
                                for i in range(x_cur, x_cur + struct_width)
                                for j in range(y_cur, y_cur + struct_height)
                })

            # add walls (can think of this as the border between structures)
            self.map.update({ (i,j):Wall(i,j)
                                for i in range(x_cur - 1, x_cur + struct_width + 1)
                                for j in [y_cur-1, y_cur+struct_height]
                                if not isinstance((i,j), Wall)
                })
            self.map.update({ (i,j):Wall(i,j)
                                for i in [x_cur-1, x_cur+struct_width]
                                for j in range(y_cur - 1, y_cur + struct_height + 1)
                                if not isinstance((i,j), Wall)
                })
            
            self.structures.append(
                StructureInfo(struct_key, x_cur, y_cur, struct_width, struct_height)
            )
        elif self.isAdded(struct_key): 
            print('%s was already added. Can only have one of its type' % (struct_key))
        else:
            print('Unable to find structure that fits in the available area at: (%s, %s)' % (x_cur, y_cur))
    
    def placeRooms(self):
        x_cur = 1
        y_cur = 1
        room_num = 0
        while y_cur < self.height - 1:
            if  isinstance(self.map[(x_cur, y_cur)], Wall) or \
                isinstance(self.map[(x_cur, y_cur)], Room):
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1
            else:
                self.placeRoom(x_cur, y_cur, room_num)
                room_num += 1
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1

        for room in self.rooms: 
            # Determine neighbors: neighbors are saved as a dictionary, with
            # the room number of the neighbor as the key and a list of tuples
            # of the coordinates of the walls between the neighbors as the value
            if room.x != 1:                                 # Check west
                for i in range(room.y, room.y + room.height):
                    if isinstance(self.map[(room.x - 2, i)], Room):
                        neighborNum = self.map[(room.x - 2, i)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (room.x-1, i)
                        )
            if room.x + room.width - 1 != self.width:       # Check east
                for i in range(room.y, room.y + room.height):
                    if isinstance(
                        self.map[(room.x + room.width + 1, i)], Room
                    ):
                        neighborNum = \
                            self.map[(room.x + room.width + 1, i)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (room.x + room.width, i)
                        )
            if room.y != 1:                                 # Check north
                for i in range(room.x, room.x + room.width):
                    if isinstance(self.map[(i, room.y - 2)], Room):
                        neighborNum = self.map[(i, room.y - 2)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (i, room.y - 1)
                        )
            if room.y + room.height - 1 != self.height:     # Check south
                for i in range(room.x, room.x + room.width):
                    if isinstance(
                        self.map[(i, room.y + room.height + 1)], Room
                    ):
                        neighborNum = \
                            self.map[(i, room.y + room.height + 1)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (i, room.y + room.height)
                        )

            # For each neighbor, if there isn't already an entrance, place an
            # entrance randomly (Maybe not at all?)

            for n in room.neighbors:
                hasEntrance = False
                # Check if there is already an entrance to the neigboring room
                for coordinate in room.neighbors[n]:
                    if isinstance(self.map[coordinate], Entrance):
                        hasEntrance = True
                # If there isn't already an entrance, place one randomly
                if not hasEntrance:
                    newEntrance = random.choice(room.neighbors[n])
                    self.map.update({ 
                        newEntrance:Entrance(newEntrance[0],newEntrance[1])
                    })

    def isAdded(self, key):
        if ((key in ['tori', 'river', 'lake', 'river', 'pavillion']) and \
            (key in [struct.key for struct in self.structures])):
            return True
        else:
            return False

    def isBuilindg(self, key):
        return key in [
            'house', 
            'pagoda', 
            'pavillion', 
            'tori'
            ]

    def isNature(self, key):
        return key in [
            'filler_1', 
            'filler_2', 
            'filler_3', 
            'lake', 
            'river', 
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
            'waterfall'
            ]
    
    def getStructures(self):
        structs = []
        for struct in self.structures:
            structs.append({
                'name': struct.key,
                'position': [struct.x, struct.y], # NOTE: Minecraft is in xz-axis so the y-coord is z in Minecraft
                'dim': STRUCTURES[struct.key]['dim'],
                'orientation': '',
                'rules': STRUCTURES[struct.key]['rules']
            })
        return structs
    
    def serializeStructures(self, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(self.getRules(), json_file, indent = 6)
    
    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.map[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"


class StructureInfo:
    def __init__(self, key, x, y, width, height):
        self.key, self.x, self.y, self.width, self.height, self.neighbors = key, x, y, width, height, {}

    def __str__(self):
        s = "Structure " + " " + self.key + " [ (" + str(self.x) + "," + str(self.y) \
            + "); " + str(self.width) + " x " + str(self.height) + " ]"
        return s