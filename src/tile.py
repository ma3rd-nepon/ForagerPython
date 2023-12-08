import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, num):
        super().__init__(groups)
        if num == 0:
            self.image = pygame.image.load('../sprites/water.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
        elif num == 1:
            self.image = pygame.image.load('../sprites/grass.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)

