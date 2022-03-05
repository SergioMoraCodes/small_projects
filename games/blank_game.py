import pygame, sys
from pygame.locals import *

pygame.init()
displaysurface=pygame.display.set_mode((600,500),0,32)
pygame.display.set_caption('Primer ventana gráfica')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
