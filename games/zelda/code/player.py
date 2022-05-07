import pygame
from entity import Entity
from settings import *
from support import import_folder
from entity import Entity
class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos) # gets rect to draw image
        self.hitbox = self.rect.inflate(0,-26)  # offset rect to make collisions

        # graphic setup
        self.import_player_assets()
        self.status = 'down'

        # movement
        self.attacking        = False
        self.attack_cooldown  = 400
        self.attack_time      = 0
        self.casting          = False
        self.cast_cooldown    = 400
        self.cast_time        = 0
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats  = {'health':100, 'energy':60, 'attack':10, 'magic':4, 'speed':5} # max
        self.health = self.stats['health'] # current
        self.energy = self.stats['energy'] # we can have a difference between current and max
        self.speed  = self.stats['speed' ]
        self.exp    = 0

        # weapon
        self.create_attack   = create_attack   #? stores the function create attack
        self.destroy_attack  = destroy_attack
        self.weapon_index    = 1
        self.weapon          = list(weapon_data.keys())[self.weapon_index]
        self.attack_switch   = True
        self.switch_cooldown = 200
        self.switch_time     = 0

        # magic
        self.create_magic   = create_magic
        self.magic_index    = 0
        self.magic          = list(magic_data.keys())[self.magic_index]
        self.magic_strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
        self.magic_cost     = list(magic_data.values())[self.magic_index]['cost']
        self.magic_switch   = True

        # timer
        self.vulnerable   = True
        self.hurt_time    = 0
        self.invulnerable = 500

    def import_player_assets(self):
        folder_path     = '../graphics/player/'

        self.animations = {
                   'up':[],        'down':[],        'left':[],        'right':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[],
            'up_idle'  :[], 'down_idle'  :[], 'left_idle'  :[],   'right_idle':[]}

        for animation in self.animations.keys():
            full_path = folder_path + animation
            self.animations[animation] = import_folder(full_path) #import all the surfaces into the dict

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            #movement input
            if   keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if   keys[pygame.K_LEFT]:
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
                self.attacking      = True
                self.attack_time    = pygame.time.get_ticks() #gets time once
                self.magic          = list(magic_data.keys())[self.magic_index]
                self.magic_strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                self.magic_cost     = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(self.magic, self.magic_strength, self.magic_cost)

            if keys[pygame.K_q] and self.attack_switch:
                self.attack_switch = False
                self.switch_time   = pygame.time.get_ticks()
                self.weapon_index += 1

                if self.weapon_index >= len(weapon_data.keys()):
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.magic_switch:
                self.magic_switch = False
                self.switch_time  = pygame.time.get_ticks()
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
                if 'idle'   in self.status:
                    self.status = self.status.replace('idle','attack')#overwrite idle
                else:
                    self.status = self.status + '_attack'

    def cooldowns(self):
        current_time = pygame.time.get_ticks() #* continuosly measure what time it's
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
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

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerable:
                self.vulnerable = True

    def get_weapon_damage(self):
        # base damage + weapon damage
        return self.stats['attack']+ weapon_data[self.weapon]['damage']

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed #continuosly add to the frame index
        if self.frame_index >= len(animation): #resets the frame
            self.frame_index = 0

        #set image
        self.image = animation[int(self.frame_index)] #changes the image looping the animation dict of surfaces
        self.rect = self.image.get_rect(center= self.hitbox.center) #we have to update the rectangle because every image is not the same size

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
