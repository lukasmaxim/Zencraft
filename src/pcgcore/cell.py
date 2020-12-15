import random

class Cell:
#   The Cell class is the superclass of all other cell classes.  It represents a
#   single cell on the level.  By itself, it represents a blank or "open space" 
#   cell
#   
#   Fields:
#       x (int):    The x coordinate of the cell on the level
#       y (int):    The y coordinate of the cell on the level
#
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return u"\u2591"

class Wall(Cell):
#   The wall class is a subclass of the Cell class.  It represents a wall on the
#   level.  By itself, it represents a wall that cannot be destroyed by the
#   player.  These walls will be used around the outer edge of each level.
    def __str__(self):
        #return u"\u2588"
        return "%"

class Structure(Cell):
    def __init__(self, x, y, symbol):
        super(Structure, self).__init__(x, y)
        self.symbol = symbol
    def __str__(self):
        return str('^')
        