import pygame, sys
from settings import *
from level import Level
from support import set_screen_prop
class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = set_screen_prop()
        # self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.sound = pygame.mixer.Sound('audio/main.ogg')
        self.sound.set_volume(0.2)
        self.sound.play(loops=-1)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        self.level.toggle_menu()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill(WATER_COLOR)
            self.level.run(int(self.clock.get_fps()))
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()