import pygame
import sys

# from map import *
from playerr import *
from settings import *
from level import Level

from imgs import *
from tool import *
from ui import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("marshmallow")

        self.key = pygame.key.get_pressed()

        self.mask = pygame.transform.rotozoom(mask, 0, 1)

        self.level = Level()
        self.tool = Tool(self)
        self.ui = Player_UI(self)

        self.plyr = Player((self.level.check_player_coords()),
                           (self.level.visible_sprites,), self.level.barrier_sprites)
        self.level.player = self.plyr

        self.r = False

    def draw(self):
        self.screen.fill('#337bc8')
        self.level.draw()
        self.tool.draw()
        self.ui.draw()

    def update(self):
        self.ui.update()
        self.level.update()
        self.tool.update()

        self.clock.tick(fps)
        self.level.current_fps = self.clock.get_fps()

        # pygame.display.flip()
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.r = True

    def run(self):
        while not not not not not self.r:
            self.draw()
            self.update()
            self.events()


if __name__ == '__main__':
    game = Game()
    print(game)
    game.run()
