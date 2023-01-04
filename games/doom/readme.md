# Doom style game in python

project develop using pygame library

### Process
1. Game setup, define settings, map creation
2. Player Creation, movement and collisions


## Process

### 1. Game Setup:

- Define setting.py file with resolution, fps, tile_size and player characteristics
  
```
# game settings
RES  = WIDTH, HEIGHT = 1280, 720
FPS  = 60
TILE = 60

# PLAYER
PLAYER_POS       = 1.5, 5 # mini_map
PLAYER_ANGLE     = 0
PLAYER_SPEED     = 0.004
PLAYER_ROT_SPEED = 0.002
```

- create main.py file and initialize pygame with a Game class

```
class Game:
    def __init__(self): #constructor which initialize pygame modules
        pg.init()
        self.screen = pg.display.set_mode(RES) # create the screen for rendering the set resolution
        self.clock  = pg.time.Clock() # instance of the clock class for framerate
        self.new_game()

    def new_game(self):
        pass # here we will create the map and the player

    def update(self):   # here we will update every entity in the game
        pg.display.flip()
        self.clock.tick(FPS)  # it sets the frame of rate
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):   # here wi will draw the map and every entity
        self.screen.fill('black')

    def check_events(self):  # checks to terminate the program
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):   # main loop of the game
        while True:  # it consist of checking events, updating and drawing the entities
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()  # create an instance of the game and run it
    game.run()
```
