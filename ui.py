import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # conver stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect, 4)

    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)), False, TETX_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surface, text_rect)

    def selection_box(self, left, top,has_swith):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_swith:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_swith):
        bg_rect = self.selection_box(20, 500, has_swith)  # weapon box
        weapon_stuf = weapon_data[list(weapon_data.keys())[weapon_index]]['graphic']
        weapon = pygame.image.load(weapon_stuf).convert_alpha()
        weapon_rect = weapon.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon, weapon_rect)

    def display(self, player):
        self.show_bar(player.healtf, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(12)
        self.weapon_overlay(player.weapon_index, player.swich_weapon)
        # self.selection_box(90, 510)  # magic box
