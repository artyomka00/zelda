import pygame
from settings import *

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
        delta = player.rect.center - self.display_center
        if delta.x > self.display_surface.get_size()[0] // 2:
            self.direction.x = -1
        if delta.x < -self.display_surface.get_size()[0] // 2:
            self.direction.x = 1
        if delta.y > self.display_surface.get_size()[1] // 2:
            self.direction.y = -1
        if delta.y < -self.display_surface.get_size()[1] // 2:
            self.direction.y = 1
        self.length += self.direction.x * self.speed_screen
        self.hieght += self.direction.y * self.speed_screen
        self.offset += self.direction * self.speed_screen
        if abs(self.length) >= WIDTH - TILESIZE * 0.5:
            self.length = 0
            if self.direction.x<0:
                self.display_center.x += self.display_surface.get_size()[0]
            else:
                self.display_center.x -= self.display_surface.get_size()[0]
            self.direction.x = 0
        if abs(self.hieght) >= HEIGTH - TILESIZE * 0.5:
            self.hieght = 0
            if self.direction.y<0:
                self.display_center.y += self.display_surface.get_size()[1]
            else:
                self.display_center.y -= self.display_surface.get_size()[1]
            self.direction.y = 0

        of_flore = self.flor_rect.topleft + self.offset
        self.display_surface.blit(self.floor_surf, of_flore)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def start(self, player):
        dx = player.rect.centerx - self.display_surface.get_size()[0] // 2
        dy = player.rect.centery - self.display_surface.get_size()[1] // 2
        dx = dx if dx > 0 else 0
        dy = dy if dy > 0 else 0

        self.offset.x = -dx
        self.offset.y = -dy
        self.display_center -= self.offset
        offset_flore = self.flor_rect.topleft+self.offset
        # self.flor_rect.topleft -= offset
        self.display_surface.blit(self.floor_surf, offset_flore)
        for sprite in self.sprites():
            offset_sprite = sprite.rect.topleft+self.offset
            # sprite.rect.topleft -= offset
            # sprite.hitbox.center = sprite.rect.center
            self.display_surface.blit(sprite.image, offset_sprite)


