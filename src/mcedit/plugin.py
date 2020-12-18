from mcedit2.plugins import registerPluginCommand, SimpleCommandPlugin
from ..frontend.main import FrontEnd

@registerPluginCommand
class ZenCraft(SimpleCommandPlugin):
    displayName = "ZenCraft"

    options = [
        {
            'type': 'text',
            'value': 'main.json',
            'name': 'dbName',
            'text': 'Database Filename',
        },
        {
            'type': 'blocktype',
            'value': 'minecraft:grass',
            'name': 'groundMaterial',
            'text': 'Ground Material'
        },
        {
            'type': 'int',
            'value': 200,
            'min': 0,
            'max': 1000,
            'name': 'planeSize',
            'text': 'Plane Size',
        },
        {
            'type': 'int',
            'value': 10,
            'min': 0,
            'max': 100,
            'name': 'yOffsetPlane',
            'text': 'Plane Height',
        },
        {
            'type': 'int',
            'value': 850,
            'min': -5000,
            'max': 5000,
            'name': 'xOffsetPlane',
            'text': 'Plane X',
        },
                {
            'type': 'int',
            'value': 250,
            'min': -5000,
            'max': 5000,
            'name': 'zOffsetPlane',
            'text': 'Plane Y',
        },
        {
            'type': 'int',
            'value': 11,
            'min': 0,
            'max': 100,
            'name': 'yOffsetStructures',
            'text': 'Structure Height',
        },
        {
            'type': 'float',
            'value': 1,
            'min': 0,
            'max': 10,
            'name': 'structurePadding',
            'text': 'Structure Padding',
        },
        {
            'type': 'int',
            'value': 5,
            'min': 0,
            'max': 500,
            'name': 'maxBuildings',
            'text': 'Max No. Buildings',
        },
        {
            'type': 'int',
            'value': 5,
            'min': 0,
            'max': 500,
            'name': 'maxNature',
            'text': 'Max No. Natural Structures',
        },
    ]

    def perform(self, dimension, selection, options):
        dimensions = [-options['planeSize']//2, options['planeSize']//2, -options['planeSize']//2, options['planeSize']//2]
        frontend = FrontEnd(options['dbName'], dimensions, options['structurePadding'], options['maxBuildings'], options['maxNature'])

        blocks = frontend.generate(options['yOffsetStructures'], options['xOffsetPlane'], options['yOffsetPlane'], options['zOffsetPlane'], options['groundMaterial'])

        for block in blocks:
            dimension.setBlock(block['x'], block['y'], block['z'], block['material'])

