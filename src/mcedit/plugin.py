from mcedit2.plugins import registerPluginCommand, SimpleCommandPlugin
from ..frontend.main import FrontEnd

@registerPluginCommand
class ZenCraft(SimpleCommandPlugin):
    displayName = "ZenCraft"

    options = [
        {
            'type': 'text',
            'value': 'mock.json',
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
            'value': 100,
            'min': 0,
            'max': 200,
            'name': 'planeSize',
            'text': 'Plane Size',
        },
        {
            'type': 'int',
            'value': 1,
            'min': 0,
            'max': 100,
            'name': 'yOffset',
            'text': 'Plane Height',
        },

    ]

    def perform(self, dimension, selection, options):
        dimensions = [-options['planeSize']//2, options['planeSize']//2, -options['planeSize']//2, options['planeSize']//2]
        frontend = FrontEnd(options['dbName'], dimensions)

        blocks = frontend.generate(options['yOffset'], options['groundMaterial'])

        for block in blocks:
            dimension.setBlock(block['x'], block['y'], block['z'], block['material'])

