import pygame

from settings import *
from imgs import *

pl_pos = 6, 3
pl_speed = 0.003
pon = [6, 3]
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

        self.index_walk = 0  # индекс анимации движения
        self.index_idle = 0  #
        self.index_dash = 0  # индекс анимации рывка (в будущем будет)
        self.hehe = 0  # я без понятия что это но для работы оно надо
        self.curr_img = pl_base

        self.tx, self.ty = False, False  # поворот игрока по х у

    def movement(self):
        """Движение игрока по WASD"""
        speed = pl_speed * self.game.delta_time  # скорость игрока (потом сделаю ускорением)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_0]:
            pass  # не убирать

        elif keys[pygame.K_d]:
            self.tx = False
            if self.x * 100 <= w - 50 and self.x * 100 < 930:
                self.x += speed
            self.animate_walk()

        elif keys[pygame.K_a]:
            self.tx = True
            if self.x * 100 > 30 and 340 < self.x * 100:
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
        """Рисует игрока"""
        self.game.screen.blit(self.player, self.hitbox_rect)

    def update(self):
        """Обновление отрисовки игрока"""
        self.movement()

    def animate_walk(self):
        """Анимация при движении"""
        self.index_walk += 0.2

        if self.index_walk >= len(im_w) or self.index_idle < 0:
            self.index_walk = 0

        self.curr_img = im_w[int(self.index_walk)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)

    def animate_idle(self):
        """Анимация когда игрок ничего не делает"""
        self.index_idle += 0.15

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

    def draw_particles(self, x: int, y: int):  # да я непонимаю че там сделать
        """Рисует партиклы пыли при движении игрока"""
        self.hehe += 0.05
        xx, yy = x, y

        if self.hehe >= 5:
            self.hehe = 0
        if int(self.hehe) == 1:
            pygame.draw.circle(self.game.screen, 'red', (xx, yy), 10)

        if int(self.hehe) == 2:
            pygame.draw.circle(self.game.screen, 'red', (xx, yy), 5)

        if int(self.hehe) == 3:
            pygame.draw.circle(self.game.screen, 'red', (xx, yy), 2)
