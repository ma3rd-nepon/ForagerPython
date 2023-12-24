import pygame, sys

# from map import *
# from player import *
from settings import *
from debug import debug
from level import Level


# from imgs import *
# from tool import *


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('white')
            self.level.run()
            pygame.display.update()
            self.clock.tick(fps)


if __name__ == '__main__':
    game = Game()
    game.run()
