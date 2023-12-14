import pygame
from settings import *
from tile import Tile
from playerr import Player
from debug import debug
from imgs import *

srpites_dict = {
    'x': cbble,
    'i': iron,
    'g': grass,
    'z': gold
}


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = YCamera()
        self.barrier_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.player = None
        self.create_map()

        self.current_fps = 0
        self.grass_rect = (0, 0, 200, 200)

    def create_map(self):
        pl = (0, 0, False)
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                # tilesize = 64
                x, y = col_index * tilesize, row_index * tilesize
                if col == 'p':
                    pl = (x, y, True)
                    continue
                if col == ' ':
                    continue
                Tile((x, y), (self.visible_sprites, self.barrier_sprites), srpites_dict[col])
        if pl[2]:
            self.player = Player((pl[0], pl[1]), (self.visible_sprites,), self.barrier_sprites)
        else:
            print('player not on map')

    def run(self):
        self.screen.fill('#337bc8')
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        pygame.draw.rect(self.screen, 'black', (0, 0, 160, 160))
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


