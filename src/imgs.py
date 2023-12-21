import pygame

from settings import *

player = pygame.image.load('../sprites/player/player.png')

tile = pygame.image.load('../sprites/tile.png')

cbble, coal, iron, gold, grass, mask = [tile.subsurface(pygame.Rect(i * tilesize, 0, tilesize, tilesize)) for i in range(tile.get_width() // tilesize)]

# инструменты
pickaxes = pygame.image.load('../sprites/tools/pickaxes.png')

pickaxe = [pickaxes.subsurface(pygame.Rect(((i * 90) + (i * 2)), 0, 90, 90)) for i in range(9)]

# юзер интерфасе
ui = pygame.image.load('../sprites/user_interface.png')
coin, heart, no_heart = [ui.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in range(3)]
hotbar = ui.subsurface(pygame.Rect(0, 100, 250, 50))
crosshair = ui.subsurface(pygame.Rect(250, 100, 35, 35))

# враги

slime = pygame.image.load('../sprites/enemy/slime/slime.png')

ghost = pygame.image.load('../sprites/enemy/form-2x12.png')
