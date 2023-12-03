import pygame

from map import *
from player import *
from settings import *
from imgs import *
from tool import *
from ui import *


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)

        self.player = None
        self.map = None
        self.tool = None
        self.ui = None

        self.game = False  # если она фолс то игра не будет работать (запустится сама после загрузочного экрана)
        self.title_image = pygame.transform.rotozoom(tilte_base, 0, 1)  # пикча загрузочного экрана
        self.current_title = tilte_base  # текущая пикча загрузочного экрана
        self.title_hb = self.title_image.get_rect(center=(w // 2, h // 2))
        self.title_i = 0  # индекс анимации загрузочного экрана
        self.title()  # функция которая этот загрузочный экран воспроизводит

        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.cross_im = crosshair  # картинка прицела
        self.cross = self.cross_im.get_rect()
        pygame.mouse.set_visible(False)
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.spawn = False  # флаг для создания блоков в рандом месте

        self.pause = False  # если тру то игра на паузе
        self.pause_image = pygame.image.load('../sprites/title/presents_1.png').convert_alpha()  # пикча паузы
        self.pause_hb = self.pause_image.get_rect(center=(w // 2, h // 2))

        self.instruct()  # пишет в консоль клавиши

    def start_game(self):
        """Определение всех классов"""
        self.map = Map(self)
        self.player = Player(self)
        self.tool = Tool(self)
        self.ui = Player_UI(self)

    def update(self):
        """Обновление всех штук изображаемых на экране"""
        if self.game:
            if not self.pause:
                self.player.update()
                self.tool.update()
                self.ui.update()
        else:
            self.title()
        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)
        # pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")
        pygame.display.set_caption("alone marshmallow")

    def draw(self):
        """Отрисовка всех штук на экране"""
        if not self.pause:
            self.screen.fill('#337bc8')
            self.map.draw()
            self.player.draw()
            self.tool.draw()
            self.ui.draw()

            # draw crosshair
            mx, my = pygame.mouse.get_pos()  # координаты мыши
            self.cross.x = mx - 15
            self.cross.y = my - 15
            self.screen.blit(self.cross_im, self.cross)
        else:
            pygame.draw.line(self.screen, 'white', (0, h // 2), (w, h // 2))

    def eventss(self):
        """Обработка событий игры"""
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
                    if not self.pause:
                        self.player.dash()

                if e.key in [97, 100, 115, 119]:
                    self.player.draw_particles(pon[0] - 20, pon[1] + 75)

                if e.key == pygame.K_9:
                    self.ui.coin_count += 1
                    print(self.ui.coin_count)

                # skip title
                if e.key == 13:
                    self.title_i = len(im_title) + 1
                if e.key == pygame.K_ESCAPE:
                    if self.game:
                        self.pause = not self.pause
                        if self.pause:
                            pause_font = pygame.font.SysFont('hooge 05_54', 30)
                            conf_font = pygame.font.SysFont('hooge 05_54', 15)
                            pause_text = pause_font.render('Game paused', False, 'white')
                            keys_text = conf_font.render('''
Configuration
  WASD - movement
  SPACE - dash
  M - create blocks (test)
  N - hit
  ESC - pause
  ENTER - title skip
  9 - +coin (test)''', False, 'white')
                            self.screen.blit(self.pause_image.convert_alpha(), self.pause_hb)
                            self.screen.blit(pause_text, (w / 2 - 150, 20))
                            self.screen.blit(keys_text, (20, h // 2 + 20))
                        else:
                            pass

    def run(self):
        """Запуск игры и её главный цикл"""
        while True:
            self.eventss()
            self.update()
            if self.game:
                self.draw()
                if self.spawn:
                    self.map.spawn_blocks()

    def instruct(self):
        """Вывод всех используемых клавиш и их назначение"""
        print('WASD - ходить')
        print('SPACE - рывок')
        print('M - создать блоки')
        print('N - удар киркой')
        print('ESC - пауза')
        print('ENTER - скип титла')
        print('9 - плюс монета (тест)')

    def title(self):
        """Экран 'представляет' вначале запуска программы"""
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
