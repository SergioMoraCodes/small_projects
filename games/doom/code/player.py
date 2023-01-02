from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle     = PLAYER_ANGLE

    def movement(self): # will be called in the update
        pass

    def update(self):
        self.movement()

    @property
    def pos(self): #returns the position of the player
        return self.x, self.y

    @property
    def map_pos(self): #returns the int coordinates of the tile we are on
        return int(self.x), int(self.y)