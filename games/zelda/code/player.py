import pygame
from settings import *
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups) #iniciando la clase padre
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(0,-26)

        # graphic setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.casting = False
        self.cast_cooldown = 400
        self.cast_time = 0
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {'health':100, 'energy':60, 'attack':10, 'magic':4, 'speed':5}
        self.health = self.stats['health'] *0.4 #we can have a difference between the maximun and current amount
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        # weapon
        self.create_attack   = create_attack #? store the function create attack
        self.destroy_attack  = destroy_attack
        self.weapon_index    = 1
        self.weapon          = list(weapon_data.keys())[self.weapon_index]
        self.attack_switch      = True
        self.switch_cooldown = 200
        self.switch_time     = 0

        # magic
        self.create_magic   = create_magic
        self.magic_index    = 0
        self.magic          = list(magic_data.keys())[self.magic_index]
        self.magic_strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
        self.magic_cost     = list(magic_data.values())[self.magic_index]['cost']
        self.magic_switch   = True


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
                self.create_attack() #calls create_attack method and creates Weapon() object
            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #gets time once
                self.magic          = list(magic_data.keys())[self.magic_index]
                self.magic_strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                self.magic_cost     = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(self.magic, self.magic_strength, self.magic_cost)
            
            if keys[pygame.K_q] and self.attack_switch:
                self.attack_switch = False
                self.switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(weapon_data.keys()):
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.magic_switch:
                self.magic_switch = False
                self.switch_time = pygame.time.get_ticks()
                self.magic_index += 1
                if self.magic_index >= len(magic_data.keys()):
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

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
        current_time = pygame.time.get_ticks() #* continuosly measure what time it's
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                if 'attack' in self.status:
                        self.status = self.status.replace('_attack','')
                        self.destroy_attack()
        if not self.attack_switch:
            if current_time - self.switch_time >= self.switch_cooldown:
                self.attack_switch = True

        # if self.casting:
        #     if current_time - self.cast_time >= self.cast_cooldown:
        #         self.casting = False
        #         if 'cast' in self.status:
        #                 self.status = self.status.replace('_cast','')
        #                 self.destroy_cast()
        if not self.magic_switch:
            if current_time - self.switch_time >= self.switch_cooldown:
                self.magic_switch = True

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
