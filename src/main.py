import pygame

from map import *
from player import *
from settings import *
from imgs import *
from tool import *


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.cross_im = crosshair
        self.cross = self.cross_im.get_rect()
        pygame.mouse.set_visible(False)
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.spawn = False

        self.instruct()

    def start_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.tool = Tool(self)

    def update(self):
        self.player.update()
        self.tool.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill('#337bc8')
        self.map.draw()
        self.player.draw()
        self.tool.draw()

        # draw crosshair
        mx, my = pygame.mouse.get_pos()
        self.cross.x = mx - 15
        self.cross.y = my - 15
        self.screen.blit(self.cross_im, self.cross)

    def eventss(self):
        for e in pygame.event.get():
            m_pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT or e.type == pygame.K_ESCAPE:
                quit()
            if e.type == 768:
                if e.key == 109:
                    self.spawn = not self.spawn
                    self.map.rechoice()
                    print('random blocks spawned!')
            if e.type == 768:
                if e.key == pygame.K_SPACE:
                    self.player.dash()

    def run(self):
        while True:
            self.eventss()
            self.update()
            self.draw()
            if self.spawn:
                self.map.spawn_blocks()

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
