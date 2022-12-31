import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player          = player
        self.attribute_nr    = len(self.player.stats)
        self.attribute_name  = list(self.player.stats.keys())
        self.font            = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # selection system
        self.selection_index = 0
        self.selection_time  = None
        self.can_move        = True

        # item creation
        self.height = self.display_surface.get_size()[1] * 0.8 #get_size returns (x,y)
        self.width  = self.display_surface.get_size()[0] // (self.attribute_nr +1)   # divided by the number of items + 1 fot the space
        self.create_items()


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr: #it can't go further to the right
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                # if self.selection_index > 5:
                #     self.selection_index = 5

            if keys[pygame.K_LEFT] and self.selection_index > 0: # won't go further to the left
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                # if self.selection_index < 0:
                #     self.selection_index = 0

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def create_items(self):
        self.items = []
        for item, index in enumerate(range(self.attribute_nr)):
            #horizontal position
            full_width = self.display_surface.get_size()[0]
            increment  = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width)//2
            #vertical position
            top = self.display_surface.get_size()[1] * 0.1
            #create object
            item = Item(left, top, self.height, self.width, index, self.font)
            self.items.append(item)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def display(self):
        self.input()
        self.selection_cooldown()
        for item in self.items:
            item.display(self.display_surface, 0, 'test', 1, 2, 3)

class Item:
    def __init__(self,l,t,h,w,index,font ): #left, top, height, width, index, font
        self.rect  = pygame.Rect(l,t,w,h)
        self.index = index
        self.font  = font

    def display(self,surface,selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR,self.rect)