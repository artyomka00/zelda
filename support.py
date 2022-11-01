from csv import reader
from os import walk
import pygame
import ctypes
from settings import *

def set_screen_prop():
    user32 = ctypes.windll.user32
    screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(screenSize)
    size = (screenSize)
    pygame.display.set_caption("Window")
    width = min(size[0], WIDTH)
    heigth = min(size[1], HEIGTH)
    return pygame.display.set_mode((width,heigth), pygame.FULLSCREEN)

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return  terrain_map

def import_folder(path):
    surface_list = []
    for _,_, img_files in walk(path):
        for imgage in img_files:
            full_path = path + '/' + imgage
            imgage_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(imgage_surf)
    return surface_list


