from settings import *
import pygame

_ = False
mappp = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, _, _, 1, 1, 1, _, _, 1, 1, _, _, _, _, _, _, 1],
    [1, 1, _, _, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, _, _, 1, 1, 1, _, _, _, _, _, _, _, 1, 1, _, 1],
    [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 1],
    [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 1],
    [1, 1, _, _, 1, 1, 1, _, _, _, _, _, _, _, 1, 1, _, 1],
    [1, 1, _, _, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, _, _, 1, 1, 1, _, _, 1, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.map = mappp
        self.w_map = {}
        self.get_map()

    def get_map(self):
        for i, row in enumerate(self.map):
            for j, valuev in enumerate(row):
                if valuev:
                    self.w_map[(j, i)] = valuev

    def draw(self):
        x = 72
        rect = pygame.rect.Rect((w // 2, h // 2, x, x))
        pygame.draw.rect(self.game.screen, 'darkgray', rect, 1)
        # [draw.rect(self.game.screen, 'darkgray', (pos[0] * x, pos[1] * x, x, x), 1)
        #  for pos in self.w_map]
