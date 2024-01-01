import pygame

from settings import *
from tile import Tile
from imgs import *
from support import *
from player import Player
from random import choice


srpites_dict = {
    '0': cbble,
    '1': coal,
    '2': iron,
    '3': gold,
    '4': grass,
    '5': 'player',
    '6': sea
}


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = Camera()
        self.barrier_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.player_position = (0, 0, False)
        self.player = None

        self.create_map()

        self.current_fps = 0
        self.grass_rect = (0, 0, 200, 200)

    def load_layer(self, file):
        """Загрузить слой карты (.csv)"""
        wmp = []
        with open(file, 'r') as file:
            w_map = file.readlines()
            for i in w_map:
                wmp.append(i.rstrip().split(','))
        return wmp

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

    def check_player_coords(self):
        if self.player_position[2]:
            return self.player_position[0], self.player_position[1]
        return 0, 0

    def draw(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # debug(self.player.direction)

    def update(self):
        self.visible_sprites.update()
        # debug(self.current_fps, self.player.direction)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displ_rect = None
        self.screen = pygame.display.get_surface()
        self.displacement = pygame.Vector2()

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
