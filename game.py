import pygame
import random

# settings
resolution = w, h = 1296, 720
fps = 60

isl_b = (300, 970, 10, 610)

pl_base = pygame.image.load('sprites/idle/player_idle1.png')

crosshair = pygame.image.load('sprites/crosshair.png')


im_w = [pygame.image.load('sprites/idle/player_idle1.png'), pygame.image.load('sprites/walk/player_walk1.png'),
        pygame.image.load('sprites/walk/player_walk2.png'), pygame.image.load('sprites/walk/player_walk3.png')]

im_i = [pygame.image.load('sprites/idle/player_idle1.png'), pygame.image.load('sprites/idle/player_idle2.png'),
        pygame.image.load('sprites/idle/player_idle3.png')]

island = pygame.image.load('sprites/island-1-test.png')

test_map = pygame.image.load('sprites/map-demo.png')

cbble = pygame.image.load('sprites/ores/cobblestone.png')
coal = pygame.image.load('sprites/ores/coal.png')
iron = pygame.image.load('sprites/ores/iron.png')
gold = pygame.image.load('sprites/ores/gold.png')


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.cross_im = crosshair
        self.cross = self.cross_im.get_rect()
        pygame.mouse.set_visible(False)
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.spawn = False

    def start_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        self.player.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill('#337bc8')
        self.map.draw()
        self.player.draw()

        # draw crosshair
        mx, my = pygame.mouse.get_pos()
        self.cross.x = mx - 15
        self.cross.y = my - 15
        self.screen.blit(self.cross_im, self.cross)

    def eventss(self):
        for e in pygame.event.get():
            m_pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT or e.type == pygame.K_ESCAPE:
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    print(m_pos)
                if e.button == 3:
                    self.spawn = not self.spawn
                    self.map.rechoice()
                    print('random blocks spawned!')

    def run(self):
        while True:
            self.eventss()
            self.update()
            self.draw()
            if self.spawn == True:
                self.map.spawn_blocks()


pl_pos = 6, 3
pl_angle = 0
pl_speed = 0.003
pon = []
scaling = 1

island_x = []
for i in range(315, 970):
    island_x.append(i)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x, self.y = pl_pos
        self.player = pygame.transform.rotozoom(pl_base.convert_alpha(), 0, scaling)
        self.hitbox_rect = self.player.get_rect(center=pl_pos)
        self.m_pos = pygame.mouse.get_pos()
        self.angle = 0

        self.index_walk = 0
        self.index_idle = 0
        self.curr_img = pl_base

        self.tx, self.ty = False, False

    def movement(self):
        speed = pl_speed * self.game.delta_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print('space')

        elif keys[pygame.K_d]:
            self.tx = False
            if self.x * 100 <= w - 50 and 315 < self.x * 100 < 930:
                self.x += speed
            self.animate_walk()

        elif keys[pygame.K_a]:
            self.tx = True
            if self.x * 100 > 30 and 340 < self.x * 100 < 970:
                self.x -= speed
            self.animate_walk()

        elif keys[pygame.K_w]:
            if self.y * 100 > 30:
                self.y -= speed
            self.animate_walk()

        elif keys[pygame.K_s]:
            if self.y * 100 <= h - 80:
                self.y += speed
            self.animate_walk()
        else:
            self.animate_idle()

        pon.clear()
        pon.append(self.x * 100)
        pon.append(self.y * 100)

        self.hitbox_rect.x = pon[0] - 30
        self.hitbox_rect.y = pon[1] - 30

    def draw(self):
        self.game.screen.blit(self.player, self.hitbox_rect)

    def update(self):
        self.movement()

    def animate_walk(self):
        self.index_walk += 0.2

        if self.index_walk >= len(im_w) or self.index_idle < 0:
            self.index_walk = 0

        self.curr_img = im_w[int(self.index_walk)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)

    def animate_idle(self):
        self.index_idle += 0.05

        if self.index_idle >= len(im_i):
            self.index_idle = 0

        self.curr_img = im_i[int(self.index_idle)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)

class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.map = island.convert_alpha()
        self.island_hb = self.map.get_rect(center=(650, 360))

        self.block = None
        self.block_x, self.block_y = None, None
        self.dict_pos = {}

        self.rechoice()

    def draw(self):
        self.game.screen.blit(island.convert_alpha(), self.island_hb)

    def spawn_blocks(self):
        for i in range(10):
            self.game.screen.blit(self.dict_pos[i][0], (self.dict_pos[i][1], self.dict_pos[i][2]))

    def rechoice(self):
        for i in range(10):
            self.block = random.choice([cbble, coal, iron, gold])
            self.block_x, self.block_y = random.randint(isl_b[0], isl_b[1] - 80), random.randint(isl_b[2] + 80, isl_b[3] - 80)
            self.dict_pos[i] = (self.block, self.block_x, self.block_y)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
