import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(group)
        self.sprite_type = sprite_type
        self.image = surface
        y_offset = HITBOX_OFFSET[sprite_type]
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
            self.hitbox = self.rect.inflate(0, y_offset)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, y_offset)
