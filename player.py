import pygame
from settings import *
from support import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, group, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(group)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # moving setup
        self.attacking = False
        self.cooldawn = 400
        self.attack_time = 0

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.healtf = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 0

        # weapon
        self.create_attack = create_attack
        self.destroy_attac = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switch_weapon_cooldown = 200
        self.switch_weapon = True
        self.switch_weapon_time = 0

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.switch_magic_time = 0
        self.switch_magic_cooldown = 200

        # enemy damage
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def input(self):
        keys = pygame.key.get_pressed()
        # moving input
        if not self.attacking:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # attaking input
            if keys[pygame.K_SPACE]:
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.attacking = True

            # magic attack
            if keys[pygame.K_RCTRL]:
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = magic_data[style]['strength'] + self.stats['magic']
                cost = magic_data[style]['cost']
                self.create_magic(style, strength, cost)
                self.attacking = True

            # switch weapon
            if keys[pygame.K_COMMA] and self.switch_weapon:
                self.switch_weapon = False
                if self.weapon_index < len(weapon_data.keys()) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.switch_weapon_time = pygame.time.get_ticks()
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # switch magic
            if keys[pygame.K_PERIOD] and self.switch_magic:
                self.switch_magic = False
                if self.magic_index < len(magic_data.keys()) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.switch_magic_time = pygame.time.get_ticks()
                self.magic = list(magic_data.keys())[self.magic_index]

        # magic input

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.y = 0
            self.direction.x = 0
            if not 'attack' in self.status:
                self.status = self.status.removesuffix('_idle') + '_attack'
        else:
            self.status = self.status.removesuffix('_attack')

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_weapon_damage(self):
        damage = self.stats['attack'] + weapon_data[self.weapon]['damage']
        return damage

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        # cooldown attack
        if self.attacking:
            if current_time - self.attack_time >= self.cooldawn + weapon_data[self.weapon]['cooldown']:
                self.destroy_attac()
                self.attacking = False
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        # cooldown switch weapon
        if not self.switch_weapon:
            if current_time - self.switch_weapon_time >= self.switch_weapon_cooldown:
                self.switch_weapon = True

        # cooldown switch magic
        if not self.switch_magic:
            if current_time - self.switch_magic_time >= self.switch_magic_cooldown:
                self.switch_magic = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

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
