import pygame

from settings import *
from imgs import *


class Player_UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.font.init()
        self.game = game

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
        self.coin_hb.x, self.coin_hb.y = 20, h - 70

        self.coin_count = 0  # колво монет
        self.coin_font = pygame.font.Font(font, 40)  # шрифт для цифры
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False,
                                                     'white', bgcolor='black')  # рендер текста

        self.fps_font = pygame.font.Font(font, 20)
        self.fps = self.fps_font.render(f"{self.game.clock.get_fps()}", False, 'white', bgcolor='black')

        # energy bar
        self.percentage = 100

    def draw(self):
        """Отрисовка всех элементов интерфейса"""
        self.game.screen.blit(self.heart_image, self.heart_hb)
        self.game.screen.blit(self.heart_image2, self.heart2_hb)
        self.game.screen.blit(self.heart_image3, self.heart3_hb)

        self.game.screen.blit(self.coin_image, self.coin_hb)
        self.game.screen.blit(self.coin_count_text, (90, h - 55))

        self.game.screen.blit(self.fps, (w - 35, 10))

        pygame.draw.rect(self.game.screen, 'black', (10, 60, 105, 30))
        self.draw_energy(self.percentage)

    def update(self):
        """Обновление интерфейса"""
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, 'white')
        self.fps = self.fps_font.render(f"{int(self.game.clock.get_fps())}", False, 'white', bgcolor='black')
        self.draw()

    def draw_energy(self, percent: int):  # работает
        """Отрисовка полоски энергии"""
        perc = float(percent / 100)
        if perc < 0:
            perc = 0
        pygame.draw.rect(self.game.screen, '#90EE90', (15, 65, 95 * perc, 20))
