from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle     = PLAYER_ANGLE

    def movement(self): # will be called in the update
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time # the movement should independent of the framerate, and we need delta time for that
        speed_sin = sin_a * speed                   # delta time is the time that has passed since the last frame
        speed_cos = cos_a * speed

        keys = pg.key.get_pressed()
        # movement
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin

        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin

        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos

        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        # self.x += dx # receiving the increments to the coordinates
        # self.y += dy
        self.check_collision(dx,dy)

        # rotation
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time

        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau # modulo division returns the remainder of the integer division
                               # in that way the angle never gets larger than tau (2*pi)

    def check_wall(self,x,y):  # checks if the coordinates are shared with the wall
        return (x,y) not in self.game.map.world_map

    def check_collision(self, dx, dy): # converting the delta into an integer and checking coordinates
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy


    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * TILE,self.y * TILE),(
            (self.x * TILE + WIDTH * math.cos(self.angle)),
            (self.y * TILE + WIDTH * math.sin(self.angle))
        ), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * TILE, self.y * TILE), 15)

    def update(self):
        self.movement()

    @property
    def pos(self): #returns the position of the player
        return self.x, self.y

    @property
    def map_pos(self): #returns the int coordinates of the tile we are on
        return int(self.x), int(self.y)