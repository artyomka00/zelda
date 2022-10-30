import pygame
from settings import *

class UI:
    def __int__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar
        self.healt_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.enerdy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def display(self, player):
        # pass
        pygame.draw.rect(self.display_surface, 'black', self.healt_bar_rect)