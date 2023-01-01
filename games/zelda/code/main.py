import pygame, sys
from settings import *
from level import Level
class Game:
    def __init__(self):

        # Basic setup to use Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating the display surface (window)
        pygame.display.set_caption('Zelda')    #  title of the window
        self.clock = pygame.time.Clock()       # creating a clock
        self.level = Level()

        #sound
        main_theme = pygame.mixer.Sound('../audio/main.ogg')
        main_theme.set_volume(0.5)
        main_theme.play(loops = -1)

    def run(self):
        while True: # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # checks if we are closing the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu ()
            self.screen.fill(WATER_COLOR) # filling the screen with a black color
            self.level.run()
            pygame.display.update()   # updating the screen
            self.clock.tick(FPS)      # controlling the frame rate

if __name__=='__main__':
    game = Game() # creating instance of the Game class
    game.run()    # run method of game class