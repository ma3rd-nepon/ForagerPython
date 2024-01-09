import pygame
from settings import *
from tile import Tile
from playerr import Player
from debug import debug
from support import *
from random import choice


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = Camera()
        self.barrier_sprites = pygame.sprite.Group()

        self.player = None
        self.create_map()

    def create_map(self):
        layouts = {
            'border': import_csv_layout('../csv_files/map1._Barrier.csv'),
            'rocks': import_csv_layout('../csv_files/map1._Rocks.csv')
        }
        graphics = {
            'rocks': import_folder('../graphics/rocks')
        }

        for key, value in layouts.items():
            for row_index, row in enumerate(value):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x, y = col_index * tilesize, row_index * tilesize
                        if key == 'border':
                            Tile((x, y), (self.barrier_sprites,), 'invisible')
                        if key == 'rocks':
                            Tile((x, y), (self.barrier_sprites, self.visible_sprites),
                                 'rocks', choice(graphics['rocks']))

        self.player = Player((4000, 4000), (self.visible_sprites,), self.barrier_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displ_rect = None
        self.screen = pygame.display.get_surface()
        self.displacement = pygame.math.Vector2()

        self.half_width = self.screen.get_size()[0] // 2
        self.half_high = self.screen.get_size()[1] // 2

        self.floor_surface = pygame.image.load('../map1.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, spr):
        self.displacement.x = spr.rect.centerx - self.half_width
        self.displacement.y = spr.rect.centery - self.half_high

        """Рисуем изображение-карту"""
        floor_pos = self.floor_rect.topleft - self.displacement
        self.screen.blit(self.floor_surface, floor_pos)

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            self.displ_rect = sprite.rect.topleft - self.displacement
            self.screen.blit(sprite.image, self.displ_rect)
