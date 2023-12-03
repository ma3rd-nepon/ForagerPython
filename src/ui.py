import pygame

from settings import *
from imgs import *


class Player_UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.font.init()
        self.game = game

        self.coin_image = pygame.transform.rotozoom(coin.convert_alpha(), 0, 0.5)
        self.heart_image = pygame.transform.rotozoom(heart.convert_alpha(), 0, 0.5)

        self.heart_hb = self.heart_image.get_rect()
        self.coin_hb = self.coin_image.get_rect()

        self.heart_hb.x, self.heart_hb.y = 20, 20
        self.coin_hb.x, self.coin_hb.y = 20, h - 70

        self.coin_count = 0
        self.coin_font = pygame.font.SysFont('hooge 05_54', 40)
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False,
                                                     'white', bgcolor='black')

    def draw(self):
        self.game.screen.blit(self.heart_image, self.heart_hb)
        self.game.screen.blit(self.coin_image, self.coin_hb)
        self.game.screen.blit(self.coin_count_text, (90, h - 55))

    def update(self):
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, 'white')
        self.draw()
