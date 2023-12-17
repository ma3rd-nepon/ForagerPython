import random

from src.old import config
from settings import *
from imgs import *

pl_speed = 0.003
pll = 6, 3
pl_pos = [6, 3]
scaling = 1

particles = []

w, a, s, d = config.up, config.left, config.down, config.right


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x, self.y = pl_pos
        self.player = pygame.transform.rotozoom(pl_base.convert_alpha(), 0, scaling)
        self.hitbox_rect = self.player.get_rect(center=pll)
        self.m_pos = pygame.mouse.get_pos()
        self.angle = 0

        self.key = pygame.key.get_pressed()

        self.index_walk = 0  # индекс анимации движения
        self.index_idle = 0  #
        self.index_dash = 0  # индекс анимации рывка (в будущем будет)
        self.hehe = 0  # я без понятия что это но для работы оно надо
        self.curr_img = pl_base

        self.tx, self.ty = False, False  # поворот игрока по х у

        self.a = 0.5  # ускорение игрока
        self.walk_speed = 0.2  # скорость обновления спрайтов при движении

        self.mask_base = mask
        self.draw_mask = True  # если тру то рисует маску

    def movement(self):
        """Движение игрока по нажатию кнопок"""
        speed = pl_speed * self.game.delta_time * self.a  # скорость игрока

        if self.key[pygame.K_0]:  # незнаю что это но для работы необходимо
            pass

        elif self.key[d] and (not self.key[a]):
            if self.tx:
                self.tx = False
                self.a = 0.5
            if self.x * 100 <= width - 50:
                self.x += speed
            self.animate_walk()

        elif self.key[a] and (not self.key[d]):
            if not self.tx:
                self.tx = True
                self.a = 0.5
            if self.x * 100 > 30:
                self.x -= speed
            self.animate_walk()

        elif self.key[w] and (not self.key[s]):
            if self.y * 100 > 30:
                self.y -= speed
            self.animate_walk()

        elif self.key[s] and (not self.key[w]):
            if self.y * 100 <= height - 80:
                self.y += speed
            self.animate_walk()

        else:
            self.animate_idle()

        pl_pos.clear()
        pl_pos.append(self.x * 100)
        pl_pos.append(self.y * 100)

        self.hitbox_rect.x = pl_pos[0] - 30
        self.hitbox_rect.y = pl_pos[1] - 30

    def draw(self):
        """Рисует игрока"""
        self.game.screen.blit(self.player, self.hitbox_rect)
        if self.draw_mask:
            self.game.screen.blit(self.game.mask, (pl_pos[0] - 34, pl_pos[1] - 50))

    def update(self):
        """Обновление отрисовки игрока"""
        self.movement()

        self.key = pygame.key.get_pressed()

    def animate_walk(self):
        """Анимация при движении"""
        self.index_walk += self.walk_speed

        self.a += 0.015

        if self.a > 1:
            self.walk_speed = 0.3
            self.a = 1

        if self.index_walk >= len(im_w) or self.index_idle < 0:
            self.index_walk = 0

        self.curr_img = im_w[int(self.index_walk)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)
        self.game.mask = pygame.transform.flip(self.mask_base, self.tx, self.ty)

    def animate_idle(self):
        """Анимация когда игрок ничего не делает"""
        self.index_idle += 0.15

        self.walk_speed = 0.2
        self.a = 0.5

        if self.index_idle >= len(im_i):
            self.index_idle = 0

        self.curr_img = im_i[int(self.index_idle)]
        self.player = pygame.transform.flip(self.curr_img, self.tx, self.ty)
        self.game.mask = pygame.transform.flip(self.mask_base, self.tx, self.ty)

    def dash(self):
        print(self.hitbox_rect)
        self.a = 1
        dash = pl_speed * self.game.delta_time * 10
        if self.key[w]:
            self.y -= dash

        if self.key[a]:
            self.x -= dash

        if self.key[s]:
            self.y += dash

        if self.key[d]:
            self.x += dash

    def draw_particles(self, x: int, y: int):
        """Рисует партиклы пыли при движении игрока"""
        if self.a == 1:
            rad = (5, 20)
        else:
            rad = (0, 1)

        particles.append([[x, y], [random.randint(0, 20) / 10 - 1, -1], random.randint(rad[0], rad[1])])

        for p in particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.2
            p[1][1] += 0.1
            # pygame.draw.circle(self.game.screen, '#dede98', p[0], int(p[2]), 5)
            pygame.draw.rect(self.game.screen, '#dede98', (p[0][0], p[0][1], p[2], p[2]))
            if p[2] <= 0:
                particles.remove(p)
