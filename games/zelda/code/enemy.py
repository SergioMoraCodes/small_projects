import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, death, add_exp):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        # graphics
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image  = self.animations[self.status][self.frame_index]

        # movement
        self.rect   = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name  = monster_name
        monster_info       = monster_data[self.monster_name]
        self.health        = monster_info['health']
        self.exp           = monster_info['exp']
        self.speed         = monster_info['speed']
        self.resistance    = monster_info['resistance']
        self.attack_damage = monster_info['damage']
        self.attack_type   = monster_info['attack_type']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        # player interaction
        self.can_attack      = True
        self.attack_cooldown = 400
        self.attack_time     = 0
        self.damage_player   = damage_player
        self.trigger_death   = death
        self.add_exp         = add_exp

        # damage timer
        self.vulnerable    = True
        self.invincibility = 400
        self.hit_time      = 0

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[]} # stores the surfaces in those folders
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys(): # the folders have the same name that the keys
            self.animations[animation] = import_folder(main_path + animation) # returns all the images as surfaces

    def get_player_dist(self, player):
        enemy_vector  = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_dist(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)

        elif self.status == 'move':
            self.direction = self.get_player_dist(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center= self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks() #* continuosly measure what time it's
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                if 'attack' in self.status:
                        self.status = self.status.replace('_attack','')
                        self.destroy_attack()
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.direction = self.get_player_dist(player)[1]
                self.health -= player.get_weapon_damage()
            else:
                    self.health -= player.get_magic_damage()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death(self.monster_name, self.rect.center)
            self.kill()
            self.add_exp(self.exp)

    def enemy_update(self,player): # this method allow me to get the player from level
        self.get_status(player)
        self.actions(player)
        self.check_death()
