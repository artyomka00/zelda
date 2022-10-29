import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        """Спрайты видимые и невидимые"""
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.map_wight, self.map_height = self.create_map()


    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                if col =='p':
                    self.player = Player((x,y), [self.visible_sprites],self.obstacle_sprites)
        return len(WORLD_MAP[0]*TILESIZE), len(WORLD_MAP*TILESIZE)


    def run(self):
        """Обнволение и отрисовка игры"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug((self.player.rect.x, self.player.rect.y))
        debug(self.visible_sprites.length,y=40)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.speed_screen = 40
        self.length = 0
        self.hieght = 0

    def custom_draw(self, player:pygame.sprite.Sprite):
        if player.rect.right > self.display_surface.get_size()[0]:
            self.offset.x = -1
        if player.rect.left < 0:
            self.offset.x = 1
        self.length += self.offset.x * self.speed_screen
        if abs(self.length) >= WIDTH - TILESIZE*1.1:
            self.length = 0
            self.offset.x = 0
        if player.rect.bottom > self.display_surface.get_size()[1]:
            self.offset.y = -1
        if player.rect.top < 0:
            self.offset.y = 1
        self.hieght += self.offset.y * self.speed_screen
        if abs(self.hieght) >= HEIGTH - TILESIZE*1.1:
            self.hieght = 0
            self.offset.y = 0

        #self.offset.x = palyer.rect.centerx - self.half_width
        #self.offset.y = palyer.rect.centery - self.half_height
        for sprite in self.sprites():
            sprite.rect.topleft += self.offset * self.speed_screen
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,sprite.rect.topleft)



