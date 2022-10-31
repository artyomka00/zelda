import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, group):
        if player.energy >= cost:
            player.healtf += strength
            player.healtf = min(player.healtf, player.stats['health'])
            player.energy -= cost
            self.animation_player.create_particle('heal',player.rect.center,group)




    def flame(self, player, cost, group):
        if player.energy >= cost:
            player.energy -= cost
            direction = pygame.math.Vector2()
            status = player.status.split('_')[0]
            if status == 'right': direction.x = 1
            elif status == 'left': direction.x = -1
            elif status == 'up': direction.y = -1
            else: direction.y = 1
            for i in range(1, 6):
                if direction.x:
                    offsex_x = direction.x * i * TILESIZE
                    x = player.rect.centerx + offsex_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particle('flame', (x,y), group)
                else:
                    offsex_y = direction.y * i * TILESIZE
                    y = player.rect.centery + offsex_y + randint(-TILESIZE//3, TILESIZE//3)
                    x = player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particle('flame', (x,y), group)
                    pass



