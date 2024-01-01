from imgs import *
from settings import *

import config
import sprite_cut

w, a, s, d = config.up, config.left, config.down, config.right

pon = []


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, barrier_sprites):
        super().__init__(groups)
        self.idle, self.walk, self.hit = player
        self.image = self.idle[0]
        self.curr_img = self.image
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.barrier_sprites = barrier_sprites

        self.index = 0
        self.tx, self.ty = False, False

        self.movement()

    def movement(self):
        """Движение по WASD"""
        key = pygame.key.get_pressed()
        if any([key[w], key[a], key[s], key[d]]):
            self.animate('walk')
            if key[d] and not key[a]:
                self.tx = False
                self.direction.x = 1

            if key[a] and not key[d]:
                self.tx = True
                self.direction.x = -1

            if key[w] and not key[s]:
                self.direction.y = -1

            if key[s] and not key[w]:
                self.direction.y = 1

        else:
            self.direction.y = 0
            self.direction.x = 0
            self.animate('idle')

        if self.direction.magnitude() != 0:  # длина вектора
            self.direction = self.direction.normalize()  # делаем его длину = 1
        self.rect.x += self.direction.x * self.speed
        self.collision('горизонтально')
        self.rect.y += self.direction.y * self.speed
        self.collision('вертикально')

        pon.clear()
        pon.append(self.rect.x)
        pon.append(self.rect.y)  # position on screen (pixels)

    def collision(self, direction):
        """Коллизия с другими обьектами"""
        if direction == 'горизонтально':
            for sprite in self.barrier_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # чел движется вправо
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:  # чел движется влево
                        self.rect.left = sprite.rect.right
        if direction == 'вертикально':
            for sprite in self.barrier_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # чел движется вниз
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # чел движется вверх
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.movement()

    def animate(self, type_animation):
        """Анимация игрока"""
        self.index += 0.15

        if self.index >= len(self.idle):
            self.index = 0

        if type_animation == 'idle':
            self.curr_img = self.idle[int(self.index)]

        if type_animation == 'walk':
            self.curr_img = self.walk[int(self.index)]

        self.image = pygame.transform.flip(self.curr_img, self.tx, self.ty)

        # self.a += 0.015
        #
        # if self.a > 1:
        #     self.walk_speed = 0.3
        #     self.a = 1

    def stop_key(self, *args):
        if any([pygame.key.get_pressed()[arg] for arg in args]):
            return False
        return True

    def player_on_map(self):
        """Координата игрока на карте"""
        size = self.image.get_size()
        return [i // tilesize for i in [pon[0] + size[0] // 2, pon[1] + size[1] // 2]]  # position on map
