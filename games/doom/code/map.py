import pygame as pg


_ = False
mini_map = [ # two dimensional array where 1 means wall and 0 is empty space
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, 1, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, 1, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, 1, _, _, _, _, 1],
    [1, 1, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, 1, 1, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
    def __init__(self, game): # gets an instance of the game class as an input for the constructor
        self.game = game
        self.mini_map  = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map): # iterate over the array and obtain the rows
            for i, value in enumerate(row):     # iterate over the rows and obtain the columns
                if value:                       # we get a (i,j) coordinates where there are walls in the map
                    self.world_map[(i,j)] = value

    def draw(self, tile): # displays the map in the screen
        #iterating each element in the world map it will draw an square
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * tile, pos[1] * tile, tile, tile), 2)
        for pos in self.world_map]