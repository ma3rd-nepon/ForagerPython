import pygame

from settings import *
from imgs import *

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
