import pygame
from settings import *

class Upgrade:
    def __init__(self, player):

        # general setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_value = player.max_stats
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
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
                self.item_list[self.selection_index].trigger(self.player)
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

    def create_items(self):
        self.item_list = []
        for item in range(self.attribute_nr):
            full_width = self.display_surface.get_size()[0]
            inc = full_width // self.attribute_nr
            left = (item * inc) + (inc - self.width) // 2
            top = self.display_surface.get_size()[1] * 0.1
            index = item
            item = Item(left, top,self.width, self.height, index, self.font)
            self.item_list.append(item)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 200:
            self.can_move = True

    def display(self):
        self.input()
        self.cooldowns()
        for index , item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.stats[name]
            max_value = self.max_value[name]
            cost = self.player.upgrade_cost[name]
            item.display_item(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, left, top, wight, height, index, font):
        self.rect = pygame.Rect(left,top,wight,height)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTION if selected else TEXT_COLOR
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop+pygame.math.Vector2(0,20))

        cost_surf = self.font.render(str(int(cost)),False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom-pygame.math.Vector2(0, 20))

        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTION if selected else BAR_COLOR
        full_height = bottom[1] - top[1]
        relative_number = value/max_value * full_height
        value_rect = pygame.Rect(top[0] -15 , bottom[1] - relative_number, 30,10)
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)

    def trigger(self, player):
        upgrade_atr = list(player.stats.keys())[self.index]
        cost = player.upgrade_cost[upgrade_atr]
        if player.stats[upgrade_atr] < player.max_stats[upgrade_atr]:
            if player.exp >= cost:
                player.exp -= cost
                player.stats[upgrade_atr] *= 1.2
                player.upgrade_cost[upgrade_atr] *= 1.4
                if player.stats[upgrade_atr] > player.max_stats[upgrade_atr]:
                    player.stats[upgrade_atr] = player.max_stats[upgrade_atr]

    def display_item(self, surface, selection_number, name, value, max_value, cost):
        if self.index == selection_number:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTION,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        self.display_names(surface,name,cost,self.index == selection_number)
        self.display_bar(surface, value, max_value,self.index == selection_number)
