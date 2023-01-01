import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface

        # offset in y to make collisions more natural
            #gives more space to move trough the trees
        y_offset = HITBOX_OFFSET[sprite_type] # we are getting sprite type from level in map creation

        if sprite_type == 'objects': # offset for objects that are bigger
            self.rect = self.image.get_rect(topleft= (pos[0],pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft= pos)

        self.hitbox = self.rect.inflate(0,y_offset)