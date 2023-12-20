import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load('../sprites/ores/cobblestone.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # if col == 0:
        #     self.image = pygame.image.load('../sprites/water.png').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        # elif col == 1:
        #     self.image = pygame.image.load('../sprites/grass.png').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)  # change size
