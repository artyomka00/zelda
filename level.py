import random

import pygame

import weapon
from enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from camera import *
from ui import UI
from weapon import Weapon
from particles import *
from magic import *
from upgrade import Upgrade


class Level:
    def __init__(self):
        """Спрайты видимые и невидимые"""
        # get display
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()  # спрайты которые атакуют
        self.attackable_sprites = pygame.sprite.Group()  # спрайты которые получают урон

        # sprite setup
        self.player = None
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')

        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            # Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), tuple([self.visible_sprites]), self.obstacle_sprites,
                                                     self.create_attack, self.destroy_weapon, self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.triger_death_paarticles,
                                      self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites, self.attack_sprites])

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def add_exp(self, amount):
        self.player.exp += amount

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_srite in collision_sprite:
                        if target_srite.sprite_type == 'grass':
                            pos = target_srite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for ieaf in range(randint(3,6)):
                                self.animation_player.create_grass_particle(pos - offset, [self.visible_sprites])
                            target_srite.kill()
                        else:
                            target_srite.get_damage(self.player, attack_sprite.sprite_type)

    def triger_death_paarticles(self, pos, particle_type):
        self.animation_player.create_particle(particle_type,pos, self.visible_sprites)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.healtf -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particle(attack_type,self.player.rect.center, self.visible_sprites)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        """Обнволение и отрисовка игры"""
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
        # debug((self.upgrade.input()))
        # debug(self.player.weapon_index, y=40)

