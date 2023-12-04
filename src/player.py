import random

import pygame

from settings import *
from imgs import *

pl_pos = 6, 3
pl_speed = 0.003
pon = [6, 3]
scaling = 1

particles = []

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

        self.index_walk = 0  # индекс анимации движения
        self.index_idle = 0  #
        self.index_dash = 0  # индекс анимации рывка (в будущем будет)
        self.hehe = 0  # я без понятия что это но для работы оно надо
        self.curr_img = pl_base

        self.tx, self.ty = False, False  # поворот игрока по х у

        self.a = 0.5  # ускорение игрока

    def movement(self):
        """Движение игрока по WASD"""
        speed = pl_speed * self.game.delta_time * self.a  # скорость игрока (потом сделаю ускорением)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_0]:
            pass

        elif keys[pygame.K_d] and (not keys[pygame.K_a]):
            if self.tx:
                self.tx = False
                self.a = 0.5
            if self.x * 100 <= w - 50 and self.x * 100 < 930:
                self.x += speed
            self.animate_walk()

        elif keys[pygame.K_a] and (not keys[pygame.K_d]):
            if not self.tx:
                self.tx = True
                self.a = 0.5
            if self.x * 100 > 30:  # and 340 < self.x * 100:
                self.x -= speed
            self.animate_walk()

        elif keys[pygame.K_w] and (not keys[pygame.K_s]):
            if self.y * 100 > 30:
                self.y -= speed
            self.animate_walk()

        elif keys[pygame.K_s] and (not keys[pygame.K_w]):
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
        """Рисует игрока"""
        self.game.screen.blit(self.player, self.hitbox_rect)

    def update(self):
        """Обновление отрисовки игрока"""
        self.movement()

    def animate_walk(self):
        """Анимация при движении"""
        self.index_walk += 0.2

        self.a += 0.015

        if self.a > 1:
            self.a = 1

        if self.index_walk >= len(im_w) or self.index_idle < 0:
            self.index_walk = 0

        self.curr_img = im_w[int(self.index_walk)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)

    def animate_idle(self):
        """Анимация когда игрок ничего не делает"""
        self.index_idle += 0.15

        self.a = 0.5

        if self.index_idle >= len(im_i):
            self.index_idle = 0

        self.curr_img = im_i[int(self.index_idle)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)

    def dash(self):
        """Рывок в сторону движения"""
        dash_speed = pl_speed * self.game.delta_time * 50
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.tx = False
            if self.x * 100 <= w - 50 and self.x * 100 < 930:
                if keys[pygame.K_SPACE]:
                    if self.tx:
                        self.x -= dash_speed
                    else:
                        self.x += dash_speed

        if keys[pygame.K_a]:
            self.tx = True
            if self.x * 100 > 30 and 340 < self.x * 100:
                if keys[pygame.K_SPACE]:
                    if self.tx:
                        self.x -= dash_speed
                    else:
                        self.x += dash_speed

        if keys[pygame.K_w]:
            if self.y * 100 > 30:
                if keys[pygame.K_SPACE]:
                    self.y -= dash_speed

        if keys[pygame.K_s]:
            if self.y * 100 <= h - 80:
                if keys[pygame.K_SPACE]:
                    self.y += dash_speed

    def draw_particles(self, x: int, y: int):
        """Рисует партиклы пыли при движении игрока"""
        key = pygame.key.get_pressed()
        if any([key[pygame.K_w], key[pygame.K_a], key[pygame.K_s], key[pygame.K_d]]) and self.a == 1:
            particles.append([[x, y], [random.randint(0, 20) / 10 - 1, -1], random.randint(5, 10)])
        else:
            particles.append([[x, y], [random.randint(0, 20) / 10 - 1, -1], random.randint(0, 1)])

        for p in particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.1
            p[1][1] += 0.1
            pygame.draw.circle(self.game.screen, '#dede98', p[0], int(p[2]))
            if p[2] <= 0:
                particles.remove(p)
