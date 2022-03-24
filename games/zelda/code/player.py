import pygame
from settings import *
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups) #iniciando la clase padre
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(0,-26)

        #graphic setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        folder_path = '../graphics/player/'
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}
        for animation in self.animations.keys():
            full_path = folder_path+animation
            self.animations[animation] = import_folder(full_path) #import all the surfaces into the dict

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            #movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #gets time once
            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #gets time once

    def get_status(self):

        #idle status
        if self.direction.x == 0 and self.direction.y==0: #check if player is moving
            if not 'idle' in self.status and not 'attack' in self.status: #check for idle and attack status already written
                self.status = self.status + '_idle'

        #attacking status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle','attack')#overwrite idle
                else:
                    self.status = self.status + '_attack'

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction =self.direction.normalize()
        self.hitbox.x += self.direction.x * speed #changes x coordinate of the surface
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: #checking sprites for collisions
                if sprite.hitbox.colliderect(self.hitbox): #if there is some collision:
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x <0: #moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks() # continuosly measure what time it's
        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            if 'attack' in self.status:
                    self.status = self.status.replace('_attack','')

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed #continuosly add to the frame index
        if self.frame_index >= len(animation): #resets the frame
            self.frame_index = 0

        #set image
        self.image = animation[int(self.frame_index)] #changes the image looping the animation dict of surfaces
        self.rect = self.image.get_rect(center= self.hitbox.center) #we have to update the rectangle because every image is not the same size


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
