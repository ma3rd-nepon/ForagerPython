from pygame import *
from map import *
from player import *
from settings import *
from imgs import *


class Game(sprite.Sprite):
    def __init__(self):
        init()
        super().__init__()
        self.screen = display.set_mode(resolution)
        self.clock = time.Clock()
        self.delta_time = 1
        self.cross_im = crosshair
        self.cross = self.cross_im.get_rect()
        mouse.set_visible(False)
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.spawn = False

    def start_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        self.player.update()
        display.flip()
        self.delta_time = self.clock.tick(fps)
        display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill('#337bc8')
        self.map.draw()
        self.player.draw()

        # draw crosshair
        mx, my = mouse.get_pos()
        self.cross.x = mx - 15
        self.cross.y = my - 15
        self.screen.blit(self.cross_im, self.cross)

    def eventss(self):
        for e in event.get():
            m_pos = mouse.get_pos()
            if e.type == QUIT or e.type == K_ESCAPE:
                quit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    print(m_pos)
                if e.button == 3:
                    self.spawn = not self.spawn
                    self.map.rechoice()
                    print('random blocks spawned!')

    def run(self):
        while True:
            self.eventss()
            self.update()
            self.draw()
            if self.spawn == True:
                self.map.spawn_blocks()


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
