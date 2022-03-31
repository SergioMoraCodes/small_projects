import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups) # initiates the Sprite class and indicate in which group the tile is
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'objects':
            self.rect = self.image.get_rect(topleft= (pos[0],pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(0,-10)