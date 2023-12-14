import pygame

from map import *
from player import *
from settings import *
from imgs import *
from tool import *
from level import *


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.instruct()

    def start_game(self):
        self.level = Level()

    def update(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill('#337bc8')

    def events(self):
        for e in pygame.event.get():
            m_pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT or e.type == pygame.K_ESCAPE:
                quit()
            if e.type == 768:
                if e.key == pygame.K_SPACE:
                    self.player.dash()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.level.run()

    def instruct(self):
        print('WASD - ходить')
        print('SPACE - рывок')
        print('M - создать блоки')
        print('N - удар киркой')


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
