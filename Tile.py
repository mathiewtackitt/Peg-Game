from Directions import Directions

class Tile:

    def __init__(self, pegged, num):
        self.pegged = pegged
        self.num = num
        self.directions = {
            Directions.NW.value: None,
            Directions.NE.value: None,
            Directions.E.value: None,
            Directions.SE.value: None,
            Directions.SW.value: None,
            Directions.W.value: None
        }

    def toString(self):
        s = str(self.num) + "\n"
        for direction in Directions:
            if self.directions[direction.value] is not None:
                s += "     " + direction.value + ": " + str(self.directions[direction.value].num) + "\n"
        return s

    def hasPeg(self):
        return self.pegged
    
    def addConnection(self, direction, tile):
        self.directions[direction.value] = tile

    def copy(self):
        return Tile(self.pegged, self.num)
