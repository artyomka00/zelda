import pygame
from settings import *

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, group):
        if player.energy >= cost:
            player.healtf += strength
            player.healtf = min(player.healtf, player.stats['health'])
            player.energy -= cost



    def flame(self):
        pass


