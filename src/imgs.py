import pygame

from sprite_cut import cut_sprite
from settings import *

none = pygame.Surface((80, 80), pygame.SRCALPHA)

# плаер
player_ref = pygame.image.load('../sprites/player/player.png')
player_idle = player_ref.subsurface(pygame.Rect(0, 0, 250, 110))
player_walk = player_ref.subsurface(pygame.Rect(0, 120, 250, 110))

tile = pygame.image.load('../sprites/tiles/items.png')

tile_list = []
h = 0
for i in range(tile.get_height() // tilesize):
    if h > tile.get_height():
        break
    t = [tile.subsurface(pygame.Rect(i * tilesize, h, tilesize, tilesize)) for i in range(tile.get_width() // tilesize)]
    tile_list.append(t)
    h += tilesize

cbble, coal, iron, gold, barrier = tile_list[0]
wood, charcoal, iron_piece, gold_ingot, mask = tile_list[1]

bruh = [cbble, coal, iron, gold, barrier, wood, charcoal, iron_piece, gold_ingot, mask]

sprites = dict()
ids = [str(i) for i in range(0, 10)]

for i in range(len(ids)):
    sprites.setdefault(ids[i], bruh[i])

island = pygame.image.load('../sprites/map.png')

# инструменты
pickaxes = pygame.image.load('../sprites/tools/pickaxes.png')

pickaxe = [pickaxes.subsurface(pygame.Rect(((i * 90) + (i * 2)), 0, 90, 90)) for i in range(9)]

none_hit_ref = pygame.image.load('../sprites/tools/none.png')
hit_none = cut_sprite(none_hit_ref, 5, 1, 80, 80)

# юзер интерфасе
ui = pygame.image.load('../sprites/user_interface.png')
coin, heart, no_heart = [ui.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in range(3)]
hotbar = ui.subsurface(pygame.Rect(0, 100, 250, 50))
crosshair = ui.subsurface(pygame.Rect(250, 100, 35, 35))

# сущности
slime_idle = pygame.image.load('../sprites/entity/enemies/slime_idle.png')

slime_walk = pygame.image.load('../sprites/entity/enemies/slime_walk.png')

ghost_image = pygame.image.load('../sprites/entity/neutral/ghost.png')

sheep_idle = pygame.image.load('../sprites/entity/neutral/sheep_idle.png')

sheep_walk = pygame.image.load('../sprites/entity/neutral/sheep_walk.png')

demon_ref = pygame.image.load('../sprites/entity/enemies/demon.png')
demon_walk = demon_ref.subsurface(pygame.Rect(0, 0, 505, 83))
demon_idle = demon_ref.subsurface(pygame.Rect(0, 93, 505, 83))
demon_hit = demon_ref.subsurface(pygame.Rect(0, 186, 505, 176))

sheep = [cut_sprite(sheep_idle, 5, 2, 80, 72), cut_sprite(sheep_walk, 4, 2, 72, 80), None]

ghost = [cut_sprite(ghost_image, 6, 2, 83, 87), cut_sprite(ghost_image, 6, 2, 83, 87), None]

slime = [cut_sprite(slime_idle, 5, 1, 80, 75), cut_sprite(slime_walk, 5, 1, 80, 75), None]

player = [cut_sprite(player_idle, 3, 1, 80, 110), cut_sprite(player_walk, 3, 1, 80, 110), None]

demon = [cut_sprite(demon_idle, 6, 1, 80, 83), cut_sprite(demon_walk, 6, 1, 80, 83), cut_sprite(demon_hit, 6, 2, 80, 83)]

mask = sprites['9']
