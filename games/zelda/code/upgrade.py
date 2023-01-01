import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player          = player
        self.attribute_nr    = len(player.stats)
        self.attribute_name  = list(player.stats.keys())
        self.max_values      = list(player.max_stats.values())
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
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1: #it can't go further to the right
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
                self.items[self.selection_index].trigger(self.player)

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
        for index, item in enumerate(self.items):
            # get attributes
            name = self.attribute_name[index]
            value = list(self.player.stats.values())[index]
            max_value = self.max_values[index]
            cost = list(self.player.upgrade_cost.values())[index]
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

class Item:
    def __init__(self,l,t,h,w,index,font ): #left, top, height, width, index, font
        self.rect  = pygame.Rect(l,t,w,h)
        self.index = index
        self.font  = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        #title
        title_surf = self.font.render(name, False, color) # which surface to draw
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20)) # what we are drawing

        #cost
        cost_surf  = self.font.render(f'{int(cost)}', False, color)
        cost_rect  = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-20))
        #draw
        surface.blit(title_surf, title_rect) # where and what to draw
        surface.blit(cost_surf, cost_rect)

    def display_bar(self,surface, value, max_value, selected):
        #drawing setup
        top    = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        #bar setup
        full_height = bottom[1] - top[1] # the origin is in the top left so the bottom is larger than the top
        relative_value = value/max_value * full_height
        value_rect = pygame.Rect(top[0]-15, bottom[1]-relative_value, 30, 10) #left, top, width, height

        #draw elements
        pygame.draw.line(surface, color, top, bottom,5) #last argument is the width
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]


    def display(self,surface,selection_num, name, value, max_value, cost):
        
        if self.index == selection_num: # if selected draw this, otherwise draw the other
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR,self.rect,4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR,self.rect,4)
        self.display_names(surface,name,cost,self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)