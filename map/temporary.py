import pygame
import sys

# from map import *
from playerr import *
from settings import *
from level import Level

from imgs import *
from tool import *


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.tool = Tool(self)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    run = False
            self.level.run()
            self.tool.update()
            pygame.display.update()
            self.clock.tick(fps)
            self.level.current_fps = self.clock.get_fps()


if __name__ == '__main__':
    game = Game()
    game.run()
