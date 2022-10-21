from math import floor, sqrt
from Directions import Directions
from Tile import Tile
import game
import shutil
import math

class Board:

    MARGIN = WIDTH = HEIGHT = RADIUS = 0

    def __init__(self, R):
        self.tiles = []

        self.MARGIN = 20
        self.WIDTH, self.HEIGHT = (800, 640)
        self.NUM_ROWS = R

        r1 = (self.WIDTH / 2 / math.cos(math.radians(30)) - self.MARGIN) / self.NUM_ROWS
        r2 = ((self.HEIGHT - self.MARGIN)/ math.ceil(self.NUM_ROWS * 1.5))
        self.RADIUS = r1 if r1 <= r2 else r2

        N = int(R * (R + 1) / 2)
        for n in range(N):
            self.tiles.append(Tile(False if n == 0 else True, n + 1))
        self.connectAll()

    def display(self):
        game.begin_graphics(self.WIDTH, self.HEIGHT)
        game.clear_screen()
        self.drawBoard()
        game.sleep(1)
    
    def getReward(self):
        actions = self.getLegalActions()
        if (len(actions) != 0): return 0.0
        num_pegs = 0
        for tile in self.tiles:
            if tile.hasPeg():   num_pegs += 1
        return (len(self.tiles) - num_pegs) / num_pegs - 1

    def getLegalActions(self):
        actions = []
        for tile in self.tiles:
            if not tile.hasPeg():   continue
            for direction in Directions:
                over_tile = tile.directions[direction.value]
                if over_tile is None:   continue
                landing_tile = over_tile.directions[direction.value]
                if landing_tile is None:   continue
                if over_tile.hasPeg() and not landing_tile.hasPeg():    
                    actions.append((tile.num, direction))
        return actions
    
    def drawBoard(self):
        K = math.floor((1 + math.sqrt(1 + 8 * len(self.tiles)) / 2) - 1)
        place_y = 0.5 * (K - 1)
        while (K > 0):
            front_index = int((K * (K - 1)) / 2) - 1
            back_index = front_index + K

            place_x = 0.5 * (K - 1)
            y = (self.RADIUS + self.RADIUS * math.sin(math.radians(30))) * place_y + self.HEIGHT / 2
            for n in range(back_index, front_index, -1):
                x = math.cos(math.radians(30)) * 2 * place_x * self.RADIUS + self.WIDTH / 2
                game.hexagon((x, y), self.RADIUS, game.formatColor(0, 0, 0), game.formatColor(1, 0, 0), 1, 0)
                if self.tiles[n].hasPeg():
                    game.circle((x, y), 0.25 * self.RADIUS, game.formatColor(0, 0, 1), game.formatColor(0, 0, 1))
                place_x -= 1
            place_y -= 1
            K -= 1

    def move(self, tile_num, direction, secs):
        tile = self.tiles[tile_num - 1]
        tile.pegged = False
        tile.directions[direction.value].pegged = False
        tile.directions[direction.value].directions[direction.value].pegged = True

        if game._canvas is not None:
            game.clear_screen()
            self.drawBoard()
            game.refresh(secs)
        return self

    def connectAll(self):
        K = 1
        num_before = 0
        while num_before < len(self.tiles):
            front_index = int((K * (K - 1)) / 2) - 1
            back_index = front_index + K

            for n in range(back_index, front_index, -1):
                if n != back_index:
                    self.tiles[n].addConnection(Directions.NE, self.tiles[n - K + 1])
                    self.tiles[n].addConnection(Directions.E, self.tiles[n + 1])
                if n != front_index + 1:
                    self.tiles[n].addConnection(Directions.W, self.tiles[n - 1])
                    self.tiles[n].addConnection(Directions.NW, self.tiles[n - K])
                num_before = K * (K + 1) / 2
                if (num_before < len(self.tiles)):
                    self.tiles[n].addConnection(Directions.SE, self.tiles[n + K + 1])
                    self.tiles[n].addConnection(Directions.SW, self.tiles[n + K])
            K += 1
            num_before = K * (K - 1) / 2
    
    def toString(self):
        K = floor((1 + sqrt(1 + 8 * len(self.tiles)) / 2) - 1)
    
        S = ""
        while (K > 0):
            front_index = int((K * (K - 1)) / 2) - 1
            back_index = front_index + K
            s = ""
            for n in range(back_index, front_index, -1):
                if self.tiles[n].hasPeg():  s = "T " + s
                else: s = "O " + s
            s = s.center(shutil.get_terminal_size().columns - 1)
            S = "\n" + s + S
            K -= 1
        return S

    def copy(self):
        new_board = Board(self.NUM_ROWS)
        for t in range(len(self.tiles)):
            new_board.tiles[t] = self.tiles[t].copy()
        new_board.connectAll()
        return new_board

    def won(self):
        pegs = 0
        for tile in self.tiles:
            if tile.pegged: pegs += 1
        
        return pegs == 1
