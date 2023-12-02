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

        self.game = False
        self.title_image = pygame.transform.rotozoom(tilte_base, 0, 1)
        self.current_title = tilte_base
        self.title_hb = self.title_image.get_rect(center=(w//2, h//2))
        self.title_i = 0
        self.title()

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
        if self.game:
            self.player.update()
            self.tool.update()
        else:
            self.title()
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
                    if self.spawn:
                        print('random blocks spawned!')
                    else:
                        print('random blocks removed!')
            if e.type == 768:
                if e.key == pygame.K_SPACE:
                    self.player.dash()
                # skip title
                if e.key == pygame.K_ESCAPE:
                    self.title_i = len(im_title) + 1

    def run(self):
        while True:
            self.eventss()
            self.update()
            if self.game:
                self.draw()
                if self.spawn:
                    self.map.spawn_blocks()

    def instruct(self):
        print('WASD - ходить')
        print('SPACE - рывок')
        print('M - создать блоки')
        print('N - удар киркой')
        print('ESC - скип титла')

    def title(self):
        self.title_i += 0.01

        if self.title_i > len(im_title):
            self.title_i = 0
            self.current_title = pygame.transform.rotozoom(im_title[-1], 0, 1)
            self.title_image = pygame.transform.flip(self.current_title.convert_alpha(), False, False)
            self.game = True
            return

        self.current_title = pygame.transform.rotozoom(im_title[int(self.title_i)].convert_alpha(), 0, 1)
        self.title_image = pygame.transform.flip(self.current_title, False, False)

        self.screen.blit(self.title_image, self.title_hb)
        self.title_hb.x = 0
        self.title_hb.y = 0


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
