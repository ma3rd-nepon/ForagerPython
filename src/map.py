import random

from settings import *
from imgs import *
import pygame


class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.map = island.convert_alpha()
        self.island_hb = self.map.get_rect(center=(650, 360))

        self.block = None
        self.block_x, self.block_y = None, None
        self.dict_pos = {}

        self.rechoice()

    def draw(self):
        self.game.screen.blit(island.convert_alpha(), self.island_hb)

    def spawn_blocks(self):
        for i in range(10):
            self.game.screen.blit(self.dict_pos[i][0], (self.dict_pos[i][1], self.dict_pos[i][2]))

    def rechoice(self):
        for i in range(10):
            self.block = random.choice([cbble, coal, iron, gold])
            self.block_x, self.block_y = random.randint(isl_b[0], isl_b[1] - 80), random.randint(isl_b[2] + 80, isl_b[3] - 80)
            self.dict_pos[i] = (self.block, self.block_x, self.block_y)
