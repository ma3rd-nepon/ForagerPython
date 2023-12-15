import pygame
from settings import *
from tile import Tile
from playerr import Player
from debug import debug
from imgs import *

srpites_dict = {
    '0': cbble,
    '3': iron,
    '5': grass,
    '2': coal,
    '1': gold,
    '4': 'player'
}


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = YCamera()
        self.barrier_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.wmp = []
        self.player = None

        self.create_map()

        self.current_fps = 0
        self.grass_rect = (0, 0, 200, 200)

    def load_layer(self, file):
        with open(file, 'r') as file:
            w_map = file.readlines()
            for i in w_map:
                self.wmp.append(i.rstrip().split(','))

    def create_map(self):
        pl = (0, 0, False)
        self.load_layer('map.csv')
        for row_index, row in enumerate(self.wmp):
            for col_index, col in enumerate(row):
                # tilesize = 64
                x, y = col_index * tilesize, row_index * tilesize
                if col == '-1':
                    continue
                if srpites_dict[col] == 'player':
                    pl = (x, y, True)
                    continue
                if col == '5':
                    Tile((x, y), (self.visible_sprites,), srpites_dict[col])
                    continue
                Tile((x, y), (self.visible_sprites, self.barrier_sprites), srpites_dict[col])
        if pl[2]:
            self.player = Player((pl[0], pl[1]), (self.visible_sprites,), self.barrier_sprites)
        else:
            print('player not on map')

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.current_fps, self.player.direction)


class YCamera(pygame.sprite.Group):
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


