import pygame

import weapon
from enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from camera import *
from ui import UI
from weapon import Weapon


class Level:
    def __init__(self):
        """Спрайты видимые и невидимые"""
        # get display
        self.display_surface = pygame.display.get_surface()

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
                                      self.obstacle_sprites, self.damage_player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_srite in collision_sprite:
                        if target_srite.sprite_type == 'grass':
                            target_srite.kill()
                        else:
                            target_srite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.healtf -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles

    def run(self):
        """Обнволение и отрисовка игры"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        # debug((self.player.rect.center))
        # debug(self.player.weapon_index, y=40)

    def start(self):
        self.visible_sprites.start(self.player)
        self.visible_sprites.update()
