import pygame
from settings import *
from tile import Tile
from playerr import Player
from debug import debug


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = Camera()
        self.barrier_sprites = pygame.sprite.Group()

        self.player = None
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(NEW_WORLD_MAP):
            for col_index, col in enumerate(row):
                x, y = col_index * tilesize, row_index * tilesize
                Tile((x, y), [self.visible_sprites], col)
                self.player = Player((10, 10), [self.visible_sprites], self.barrier_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displ_rect = None
        self.screen = pygame.display.get_surface()
        self.displacement = pygame.Vector2()

        self.half_width = self.screen.get_size()[0] // 2
        self.half_high = self.screen.get_size()[1] // 2

    def custom_draw(self, player):
        self.displacement.x = player.rect.centerx - self.half_width
        self.displacement.y = player.rect.centery - self.half_high

        for sprite in self.sprites():
            self.displ_rect = sprite.rect.topleft - self.displacement
            self.screen.blit(sprite.image, self.displ_rect)
