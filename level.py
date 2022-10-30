import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from camera import *


class Level:
    def __init__(self):
        """Спрайты видимые и невидимые"""
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
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
                            Tile((x, y), [self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
        self.player = Player((1200, 1200), tuple([self.visible_sprites]), self.obstacle_sprites)

    def run(self):
        """Обнволение и отрисовка игры"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug((self.player.rect.center))
        # debug(self.test_tile.rect.center, y=40)
        debug(self.visible_sprites.offset, y=80)

    def start(self):
        self.visible_sprites.start(self.player)
        self.visible_sprites.update()



