# Zelda style game in Python

Credits to: [Clear Code Youtube Channel](https://www.youtube.com/c/ClearCode/featured), I followed a [tutorial](https://www.youtube.com/watch?v=QU1pPzEGrqw&t=9028s) to make this project, it was amazingly very clear, and easy to code along with his explanation, all the assets were included in the tutorial, so credits to the artists as well [Pixel-Boy](https://twitter.com/2Pblog1) and [AAA](https://www.instagram.com/challenger.aaa/?hl=fr).

The project was develop using pygame library.

#### Process
1. Game Setup
2. [Level Setup](#2-level-setup)
3. [Player creation](#3-player-creation)
4. [Camera](#4-creating-the-camera)
5. [Graphics](#5-graphics)
6. [Player animations](#6-player-animation)
7. [Weapons and UI](#7-weapons-and-ui)
8. Enemies and interactions
---

## Process

### 1. Game Setup:

- Initialize pygame and create a window where we are going to display the entire game, every element is "draw" in this surface.
- Also creates a clock that determines the main event loop and it's element updates.

```
import pygame, sys

class Game:
    def __init__(self):
        #! Basic setup to use Pygame
        pygame.init() #initiating pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating the display surface (window)
        pygame.display.set_caption('Zelda')    #  title of the window
        self.clock = pygame.time.Clock()       # creating a clock

    def run(self):
        while True: # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # checks if we are closing the game
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')          # filling the screen with a black color
            pygame.display.update()            # updating the screen
            self.clock.tick(FPS)               # controlling the frame rate

if __name__=='__main__':
    game = Game()                              # creating instance of the Game class
    game.run()                                 # run method of game class
```

![](/images/window.png)

### 2. Level Setup:

- Central part of the entire game, contains all the game elements like the player, enemies, and the level map, managing their interactions as sprites.

- When we create an element its created as a sprite, every sprite it's contained in a group that determine its functionality.
- A sprite can be in multiple groups at the same time.

- In a new file called `level.py` we create a new class that will be use in the main event loop

```
class Level():
    def__init__(self):
        Here there will be all the game elements as attributes, of the Level class

    def run(self):
        update and draw the game
```

- creating a sprite group `self.obstacle_sprites = pygame.sprite.Group()`

- creating the map `def create_map():` and drawing the basic elements:

![](\images\rocks.png 'basic elements displayed')



### 3. Creating the player:

  - Then we grant the player sprite, movement and collisions with the `obstacles_sprites.Group()`

### 4. Creating the camera:

- What a **sprite group** does:
    : 1. **stores** a lot of different sprites
      1. calls the **update method** `sprite.update()`
      2. calls **draw method**, which displays the sprite into the surface:
          - `surface.blit(sprite.image, sprite.rect)`
          - the ==image== is drawn in the sprite ==rectangle==

- We create a custom sprite group called `YsortCameraGroup`, that way we can create a **custom_draw method**
- We use a 2 dimensional vector `[x,y]` to offset the player ==rectangle== and draw the ==image== wherever we want
- This offset is essentially our camera, because it determines were the sprites are going to be drawn
- We get the offset from the player, in that way, the camera is following the player


### 5. Graphics:

- Import all the assets:

![](/images/map.png 'map')
![](/images/player.png 'player')
![](/images/objects.png 'obstacles')
![](/images/object1.png 'obstacles')
![](/images/grass.png 'grass')


### 6. Player animation:

- Define current **player status**
  - idle
  - walking
  - attacking

- Define the **player direction**
  - left
  - right
  - up
  - down

- Every combination of status/direction has a package of images, for which we can animate our player

### 7. Weapons and UI:

- import weapons assets and display them whenever the player attacks:

    : ![](/images/idle.png)    ![](/images/attacking.png) 
    ![](/images/down.png)    ![](/images/downattack.png)

- Create a Health bar and a Mana bar status:
- Create weapon and magic box:
 ![](/images/ui.png)

### 8. Enemies and interactions:

### 9. Spells and particles:

### 10. Menu, sound and final fixes:
