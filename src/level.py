from csv import reader
from os import walk
from tile import Tile
from imgs import *


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
        with open(file, 'r') as layer:
            layout = reader(layer, delimiter=',')
            for row in layout:
                wmp.append(row)
        return wmp

    def load_folder(self, file):
        """Загрузить файлы из папки"""
        textures_list = []
        for data in walk(file):
            _, __, images_list = data
            for image in images_list:
                image_file = file + '/' + image
                texture = pygame.image.load(image_file).convert_alpha()
                textures_list.append(texture)
        return textures_list

    def create_map(self):
        wmp = self.load_layer('../sprites/tiles/items.csv')

        for row_index, row in enumerate(wmp):
            for col_index, col in enumerate(row):
                x, y = col_index * tilesize, row_index * tilesize
                if col == '-1':
                    continue
                if col == '9':
                    self.player_position = (x, y, True)
                    continue
                if col == '4':
                    Tile((x, y), (self.barrier_sprites,), sprites[col])
                    continue
                Tile((x, y), (self.visible_sprites, self.barrier_sprites), sprites[col])

        trwmp = self.load_layer('../sprites/tiles/trees.csv')
        for row_index, row in enumerate(trwmp):
            for col_index, col in enumerate(row):
                x, y = col_index * tilesize, row_index * tilesize
                if col == '-1':
                    continue
                Tile((x, y), (self.visible_sprites, self.barrier_sprites), tree_sprites[col])

    def check_player_coords(self):
        if self.player_position[2]:
            return self.player_position[0], self.player_position[1]
        return 0, 0

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displ_rect = None
        self.screen = pygame.display.get_surface()
        self.displacement = pygame.Vector2()

        self.half_width = self.screen.get_size()[0] // 2
        self.half_high = self.screen.get_size()[1] // 2

        self.floor_surface = island.convert_alpha()
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
