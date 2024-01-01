import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, texture, sprite_type, surface=pygame.Surface((tilesize, tilesize))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = texture
        self.surf = surface
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, -20)
