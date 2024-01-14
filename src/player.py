import pygame.mixer

from imgs import *
from settings import *

import config
import sprite_cut

w, a, s, d = config.up, config.left, config.down, config.right

pon = []


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, groups, barrier_sprites):
        super().__init__(groups)
        pygame.mixer.init()
        self.idle, self.walk, self.hit = player
        self.image = self.idle[0]
        self.curr_img = self.image
        self.rect = self.image.get_rect(topleft=pos)

        self.game = game

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.barrier_sprites = barrier_sprites

        self.index = 0
        self.tx, self.ty = False, False
        self.sound_wait = 0
        self.step_sound = pygame.mixer.Sound('../sound/player/03_Step_grass_03.wav')

        self.can_animate = True

        self.movement()

    def movement(self):
        """Движение по WASD"""
        key = pygame.key.get_pressed()
        if any([key[w], key[a], key[s], key[d]]) and not self.game.ui.show[1]:
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
        rect = pygame.Rect(self.rect.topleft[0], self.rect.midleft[1], 80, 55)

        if direction == 'горизонтально':
            for sprite in self.barrier_sprites:
                if sprite.rect.colliderect(rect):
                    if self.direction.x > 0:  # чел движется вправо
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:  # чел движется влево
                        self.rect.left = sprite.rect.right
        if direction == 'вертикально':
            for sprite in self.barrier_sprites:
                if sprite.rect.colliderect(rect):
                    if self.direction.y > 0:  # чел движется вниз
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # чел движется вверх
                        if sprite.rect.top <= self.rect.centery <= sprite.rect.bottom:
                            print('aslkd')
                            self.rect.centery = sprite.rect.bottom

    def update(self):
        self.movement()

    def animate(self, type_animation):
        """Анимация игрока"""
        if self.can_animate:
            self.index += 0.15
            self.sound_wait += 0.05

            if self.index >= len(self.idle):
                self.index = 0

            if int(self.sound_wait) >= 1 and type_animation == 'walk':
                self.sound_wait = 0
                self.step_sound.play()

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
