import pygame
from settings import *

class Upgrade:
    def __init__(self, player):

        # general setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.display_surface.get_size()[0] * 0.8
        self.width = self.display_surface.get_size()[1] // 6
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_d] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_a] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                return self.selection_index

    def create_items(self):
        self.item_list = []
        for item in range(self.attribute_nr):
            full_width = self.display_surface.get_size()[0]
            inc = full_width // self.attribute_nr
            left = (item * inc) + (inc - self.width)
            top = self.display_surface.get_size()[1] * 0.1
            index = item
            item = Item(left, top,self.width, self.height, index, self.font)
            self.item_list.append(item)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 300:
            self.can_move = True

    def display(self):
        self.input()
        self.cooldowns()
        for item in self.item_list:
            item.display_item(self.display_surface, 0, 'test', 1, 2, 3)


class Item:
    def __init__(self, left, top, wight, height, index, font):
        self.rect = pygame.Rect(left,top,wight,height)
        self.index = index
        self.font = font

    def display_item(self, surface, selection_number, name, value, max_value, cost):
        pygame.draw.rect(surface,UI_BG_COLOR,self.rect)

