import pygame
from settings import weapon_data

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups) #al iniciar la clase padre debo poner a que grupos pertenece

        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0] #player status is a string, when splitted i get a two element list

        #graphic
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement                                                       adding to the (x,y) coordinates
        if   direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))#correcting weapon position the hand is below the center
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))