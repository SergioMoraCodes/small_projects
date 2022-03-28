import pygame
from settings import *

class UI():
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface() #get access to the display surface
        self.font =  pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALT_BAR_WIDTH,BAR_HEIGHT) # (left,top,width,height)
        self.energy_bar_rect = pygame.Rect(10,35,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        # converting weapons dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        #draw background
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect) # (surface,color,rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = (bg_rect.width) * ratio
        current_rect = pygame.Rect(bg_rect.left,bg_rect.top,current_width,BAR_HEIGHT)
            #could also do current_rect = bg_rect.copy() & current_rect.width = current_width
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)#(info,AA,color)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 40
        text_rect = text_surf.get_rect(bottomright=(x,y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect) # (source, dest: coordinates | can be a rect )
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

    def selection_box(self,left,top,switch):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,bg_rect)
        if switch:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,switch):
        bg_rect = self.selection_box(10,600,switch)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center= bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, magic_index, switch):
        bg_rect = self.selection_box(80,610,switch)
        magic_surface = self.magic_graphics[magic_index]
        magic_rect = magic_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surface, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index,not player.attack_switch)
        self.magic_overlay(player.magic_index,not player.magic_switch)