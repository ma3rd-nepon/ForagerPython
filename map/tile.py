import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, texture):
        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_rect(topleft=pos)
