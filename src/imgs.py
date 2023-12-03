import pygame

# кадры движения
pl_base = pygame.image.load('../sprites/player/idle/player_idle1.png')

im_w = [pygame.image.load('../sprites/player/idle/player_idle1.png'), pygame.image.load(
    '../sprites/player/walk/player_walk1.png'),
        pygame.image.load('../sprites/player/walk/player_walk2.png'), pygame.image.load(
        '../sprites/player/walk/player_walk3.png')]

im_i = [pygame.image.load('../sprites/player/idle/player_idle1.png'), pygame.image.load(
    '../sprites/player/idle/player_idle2.png'),
        pygame.image.load('../sprites/player/idle/player_idle3.png')]


# прочее
crosshair = pygame.image.load('../sprites/crosshair.png')

island = pygame.image.load('../sprites/island-1-test.png')

test_map = pygame.image.load('../sprites/map-demo.png')


# спрайты блоков
cbble = pygame.image.load('../sprites/ores/cobblestone.png')
coal = pygame.image.load('../sprites/ores/coal.png')
iron = pygame.image.load('../sprites/ores/iron.png')
gold = pygame.image.load('../sprites/ores/gold.png')


# спрайты кирки (да он один)
pickaxe_1 = pygame.image.load('../sprites/tools/pickaxe_1.png')


# загрузочный екран
im_title = [pygame.image.load('../sprites/title/presents_1.png'), pygame.image.load('../sprites/title/presents_1.png'),
            pygame.image.load('../sprites/title/presents_1.png'), pygame.image.load('../sprites/title/presents_2.png'),
            pygame.image.load('../sprites/title/presents_3.png'), pygame.image.load('../sprites/title/presents_4.png'),
            pygame.image.load('../sprites/title/ALPHAS.png')]

tilte_base = pygame.image.load('../sprites/title/presents_1.png')


# юзер интерфасе
heart = pygame.image.load('../sprites/ui/heart.png')
no_heart = pygame.image.load('../sprites/ui/heart_minus.png')
coin = pygame.image.load('../sprites/ui/coin.png')
