import pygame
from settings import *
from enemy import Enemy

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.speed_screen = 40
        self.length = 0
        self.hieght = 0
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.flor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.display_center = pygame.math.Vector2(self.display_surface.get_size()[0] // 2,
                                                  self.display_surface.get_size()[1] // 2)
        self.direction = pygame.math.Vector2()
    def custom_draw(self, player):

        dx = player.rect.centerx - self.display_surface.get_size()[0] // 2
        dy = player.rect.centery - self.display_surface.get_size()[1] // 2
        offset = pygame.math.Vector2((dx,dy))
        of_flore = self.flor_rect.topleft - offset
        self.display_surface.blit(self.floor_surf, of_flore)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        ememy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in ememy_sprites:
            enemy.enemy_update(player)

