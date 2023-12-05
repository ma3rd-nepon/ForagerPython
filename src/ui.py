import pygame

from settings import *
from imgs import *
from src import config


class Player_UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.font.init()
        self.game = game

        self.ui_screen = pygame.Surface((width, height), pygame.SRCALPHA)

        self.pause_ui = pygame.Surface((width, height), pygame.SRCALPHA)

        self.coin_image = pygame.transform.rotozoom(coin.convert_alpha(), 0, 0.5)

        self.heart_image = pygame.transform.rotozoom(heart.convert_alpha(), 0, 0.35)
        self.heart_image2 = self.heart_image
        self.heart_image3 = self.heart_image

        self.heart_hb = self.heart_image.get_rect()
        self.heart2_hb = self.heart_image2.get_rect()
        self.heart3_hb = self.heart_image3.get_rect()
        self.coin_hb = self.coin_image.get_rect()

        self.heart_hb.x, self.heart_hb.y = 10, 10
        self.heart2_hb.x, self.heart2_hb.y = 48, 10
        self.heart3_hb.x, self.heart3_hb.y = 86, 10
        self.coin_hb.x, self.coin_hb.y = 20, height - 70

        self.coin_count = 0  # колво монет
        self.coin_font = pygame.font.Font(font, 40)  # шрифт для цифры
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False,
                                                     'white', bgcolor='black')  # рендер текста

        self.fps_font = pygame.font.Font(font, 20)
        self.fps = self.fps_font.render(f"{self.game.clock.get_fps()}", False, 'white', bgcolor='black')

        # energy bar
        self.percentage = 100

        # timer
        self.time = [12, 0]
        self.imdxxx = 0

        self.hb_things = []

        self.key = pygame.key.get_pressed()

        self.show_hud = False

    def draw(self):
        """Отрисовка всех элементов интерфейса"""
        self.ui_screen.blit(self.heart_image, self.heart_hb)
        self.ui_screen.blit(self.heart_image2, self.heart2_hb)
        self.ui_screen.blit(self.heart_image3, self.heart3_hb)

        self.ui_screen.blit(self.coin_image, self.coin_hb)
        self.ui_screen.blit(self.coin_count_text, (90, height - 55))

        self.ui_screen.blit(self.fps, (width - 35, 10))

        self.draw_energy(self.percentage)

        self.draw_timer()

        if self.show_hud:
            self.game.screen.blit(self.ui_screen, (0, 0))

    def update(self):
        """Обновление интерфейса"""
        if self.coin_count > 10000:
            self.coin_count = 10000

        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, 'white', bgcolor='black')
        self.fps = self.fps_font.render(f"{int(self.game.clock.get_fps())}", False, 'white', bgcolor='black')

        self.draw()

    def draw_energy(self, percent: int):
        """Отрисовка полоски энергии"""
        perc = float(percent / 100)
        if perc < 0:
            perc = 0
        pygame.draw.rect(self.ui_screen, 'black', (10, 60, 105, 30))
        pygame.draw.rect(self.ui_screen, '#90EE90', (15, 65, 95 * perc, 20))

    def draw_timer(self):
        """Отображает игровое время"""
        timee = self.fps_font.render(f"{self.time[0]}:{str(self.time[1])}", False, 'white', bgcolor='black')
        self.ui_screen.blit(timee, (width - 80, 40))

        self.imdxxx += 0.3  # скорость течения времени ( игровая минута != секунда реальная)
        if int(self.imdxxx) == 60:
            self.imdxxx = 0
            self.time[1] += 1

        if self.time[1] == 60:
            self.time[1] = 0
            self.time[0] += 1
            self.imdxxx = 0
            if self.time[0] == 24:
                self.time[0] = 00
