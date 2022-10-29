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
        self.create_map()


    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                if col =='p':
                    self.player = Player((x,y), [self.visible_sprites],self.obstacle_sprites)


    def run(self):
        """Обнволение и отрисовка игры"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug((self.player.rect.x, self.player.rect.y))
        debug(self.visible_sprites.display_surface.get_size()[0],y=40)
        debug((self.visible_sprites.offset.x,self.visible_sprites.surface_x) ,y=80)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.surface_y = 1
        self.surface_x = 1

    def custom_draw(self, player):
        if player.rect.bottom > self.display_surface.get_size()[1] * self.surface_y :
            self.offset.y =  self.display_surface.get_size()[1] * self.surface_y
            self.surface_y += 1
        if player.rect.top < self.display_surface.get_size()[1] * self.surface_y :
            self.surface_y -= 1
            self.offset.y =  self.display_surface.get_size()[1] * self.surface_y

        if player.rect.x > (self.display_surface.get_size()[0] * self.surface_x):
            self.offset.x = self.display_surface.get_size()[0] * self.surface_x
            self.surface_x += 1
        if player.rect.x < (self.display_surface.get_size()[0] * (self.surface_x-1)):
            self.surface_x -= 1
            self.offset.x = self.display_surface.get_size()[0] * (self.surface_x-1)


        #self.offset.x = palyer.rect.centerx - self.half_width
        #self.offset.y = palyer.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)


