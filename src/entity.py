import random

import pygame.sprite

from config import Configuration

from level import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, barrier_group, can_attack, anims, coords):
        super().__init__()
        pygame.mixer.init()
        self.game = game
        self.barrier_sprites = barrier_group

        self.idle, self.walk, self.hit = anims
        self.cur_f = 0
        self.image = self.idle[0]
        self.current_image = self.image
        self.rect = self.image.get_rect()

        self.wmp = self.game.level.load_layer('map.csv')

        self.width, self.height = len(self.wmp[0]), len(self.wmp)

        self.x, self.y = None, None

        self.index = 0
        self.ppp = 0
        self.action = self.action_definition()

        self.flipx, self.flipy = False, False

        self.can_attack = can_attack

        self.uid = (f'{self.rect.x}{self.rect.y}{self.rect.width}{self.rect.height}'
                    f'{"".join(random.sample("1234567890", 2))}')

        self.def_pos(coords)

    def def_pos(self, pos: tuple):
        """Определяет позицию для сущности """
        self.x = random.randint(0, self.width - 1) if pos[0] == 'random' else pos[0]
        self.y = random.randint(0, self.height - 1) if pos[1] == 'random' else pos[1]

        if self.wmp[self.y][self.x] == '-1':
            self.rect.x = self.x * tilesize
            self.rect.y = self.y * tilesize
            return
        self.def_pos(pos)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        if not self.game.ui.show[1]:
            self.move()
            self.flip()
            self.chase(self.can_attack)

            if pygame.Rect.colliderect(self.rect, self.game.plyr.rect) and self.can_attack:
                self.action[0] = 'кусаем'

    def move(self):
        """Движение сущности"""
        cof = 4
        if self.action[0] == 'стоим':
            self.animate(self.idle)
            self.index += 1
            if self.index >= 60:
                self.index = 0
                self.action = self.action_definition()

        if self.action[0] == 'идем':
            self.animate(self.walk)
            self.index += 2
            if self.index == 60:
                self.index = 0
                self.action = self.action_definition()

            self.rect.x += cof * self.action[1]
            self.x = self.rect.x // tilesize
            self.collision('x')
            self.rect.y += cof * self.action[2]
            self.y = self.rect.y // tilesize
            self.collision('y')

        if self.action[0] == 'кусаем':
            self.animate(self.hit)
            self.index += 2
            if self.index >= 120:
                if pygame.Rect.colliderect(self.rect, self.game.plyr.rect):
                    self.game.ui.health -= 20

                self.index = 0
                self.action = self.action_definition()

    def action_definition(self):
        """Определение действия сущности (идти или стоять)"""
        return [random.choice(['идем', 'стоим']), random.randint(-1, 1), random.randint(-1, 1)]

    def flip(self):
        """Поворот в сторону движения"""
        if self.action[1] == -1:
            self.flipx = True
        elif self.action[1] == 1:
            self.flipx = False  # asjfk
    
    def collision(self, direct):
        """Коллизия с обьектами"""
        for sprite in self.barrier_sprites:
            if sprite.rect.colliderect(self.rect):
                if direct == 'x':
                    if self.action[1] == -1:
                        self.rect.left = sprite.rect.right
                    if self.action[1] == 1:
                        self.rect.right = sprite.rect.left

                if direct == 'y':
                    if self.action[2] == -1:
                        self.rect.top = sprite.rect.bottom
                    if self.action[2] == 1:
                        self.rect.bottom = sprite.rect.top

    def enemy_on_screen(self):
        """Проверить есть ли сущность на экране"""
        eom = (self.rect.x // tilesize, self.rect.y // tilesize)
        pom = self.game.plyr.player_on_map()
        if all([pom[0] - 8 <= eom[0] <= pom[0] + 8, pom[1] - 5 <= eom[1] <= pom[1] + 5]):
            return True
        return False

    def animate(self, anim: list):
        if anim:
            self.cur_f += 0.2

            if self.cur_f >= len(anim):
                self.cur_f = 0

            self.current_image = anim[int(self.cur_f)]
            self.image = pygame.transform.flip(self.current_image, self.flipx, self.flipy)
        else:
            self.animate(self.idle)

    def chase(self, is_enemy):
        if is_enemy:
            pp = self.game.plyr.player_on_map()
            en = [self.x, self.y]
            blocks = 3  # расстояние на котором видят враги

            if pp[0] - blocks <= en[0] <= pp[0] + blocks and \
                    pp[1] - blocks <= en[1] <= pp[1] + blocks and \
                    self.action[0] != 'кусаем':

                self.ppp += 1

                if pp[0] < en[0]:
                    self.action[1] = -1
                if pp[0] > en[0]:
                    self.action[1] = 1
                if pp[0] == en[0]:
                    self.action[1] = 0

                if pp[1] < en[1]:
                    self.action[2] = -1
                if pp[1] > en[1]:
                    self.action[2] = 1
                if pp[1] == en[1]:
                    self.action[2] = 0

                self.action[0] = 'идем'


class Object(pygame.sprite.Sprite):
    def __init__(self, game, text: str, action, id, draw: bool, coords: tuple):
        super().__init__()
        self.x, self.y = coords
        self.game = game
        self.text = text
        self.action = action
        self.image = id
        self.rect = self.image.get_rect()
        self.draw_m = draw
        self.config = Configuration()

    def draw(self):
        if self.draw_m:
            self.game.screen.blit(self.image, self.rect)

    def update(self):
        if self.draw_m:
            self.rect.x = self.x * tilesize
            self.rect.y = self.y * tilesize
            if self.rect.colliderect(self.game.plyr.rect):
                self.draw_text()
                if pygame.key.get_pressed()[self.config.hit]:
                    self.action(self.image)
                    self.rect.x, self.rect.y = 2147483646, 2147483646
                    self.draw_m = False

    def draw_text(self):
        rect = pygame.rect.Rect(width // 2 - 50, height // 2 - 50, 100, 20)
        fon = pygame.font.Font(None, 25)
        text = fon.render(self.text, False, 'white', 'black')
        self.game.screen.blit(text, rect)


class Boss(pygame.sprite.Sprite):
    def __init__(self, game, coords: tuple, anims: list, limit):
        super().__init__()
        self.game = game
        self.limit = limit
        self.coords = coords
        self.idle, self.walk, self.hit = anims
        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -10000 * tilesize, -10000 * tilesize

        self.cur_f = 0
        self.image = self.idle[0]
        self.current_image = self.image
        self.rect = self.image.get_rect()

        self.wmp = self.game.level.load_layer('map.csv')

        self.width, self.height = len(self.wmp[0]), len(self.wmp)

        self.index = 0
        self.ppp = 0
        self.action = self.action_definition()

        self.flipx, self.flipy = False, False

        self.uid = (f'{self.rect.x}{self.rect.y}{self.rect.width}{self.rect.height}'
                    f'{"".join(random.sample("1234567890", 2))}boss')

        self.health = self.limit
        self.letsgo = False
        self.x, self.y = -10000, -10000

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        if not self.game.ui.show[1]:
            if self.letsgo:
                self.rect.x, self.rect.y = self.coords[0] * tilesize, self.coords[1] * tilesize
                self.letsgo = False
            self.move()
            self.flip()
            if self.health != self.limit:
                self.chase()

            if pygame.Rect.colliderect(self.rect, self.game.plyr.rect) and self.health != self.limit:
                self.action[0] = 'кусаем'
            if self.health <= 0:
                self.rect.x, self.rect.y = -10000 * tilesize, -10000 * tilesize

    def move(self):
        """Движение сущности"""
        cof = 3
        if self.action[0] == 'стоим':
            self.animate(self.idle)
            self.index += 1
            if self.index >= 60:
                self.index = 0
                self.action = self.action_definition()

        if self.action[0] == 'идем':
            self.animate(self.walk)
            self.index += 2
            if self.index == 60:
                self.index = 0
                self.action = self.action_definition()

            self.rect.x += cof * self.action[1]
            self.x = self.rect.x // tilesize
            # self.collision('x')
            self.rect.y += cof * self.action[2]
            self.y = self.rect.y // tilesize
            # self.collision('y')

        if self.action[0] == 'кусаем':
            self.animate(self.hit)
            self.index += 2
            if self.index >= 120:
                if pygame.Rect.colliderect(self.rect, self.game.plyr.rect):
                    self.game.ui.health -= 20

                self.index = 0
                self.action = self.action_definition()

    def action_definition(self):
        return [random.choice(['идем', 'стоим']), random.randint(-1, 1), random.randint(-1, 1)]

    def flip(self):
        if self.action[1] == -1:
            self.flipx = True
        elif self.action[1] == 1:
            self.flipx = False  # asjfk

    def animate(self, anim: list):
        if anim:
            self.cur_f += 0.2

            if self.cur_f >= len(anim):
                self.cur_f = 0

            self.current_image = anim[int(self.cur_f)]
            self.image = pygame.transform.flip(self.current_image, self.flipx, self.flipy)
        else:
            self.animate(self.idle)

    def chase(self):
        pp = self.game.plyr.player_on_map()
        en = [self.x, self.y]
        blocks = 10  # расстояние на котором видят враги

        if pp[0] - blocks <= en[0] <= pp[0] + blocks and \
                pp[1] - blocks <= en[1] <= pp[1] + blocks and \
                self.action[0] != 'кусаем':

            self.ppp += 1

            if pp[0] < en[0]:
                self.action[1] = -1
            if pp[0] > en[0]:
                self.action[1] = 1
            if pp[0] == en[0]:
                self.action[1] = 0

            if pp[1] < en[1]:
                self.action[2] = -1
            if pp[1] > en[1]:
                self.action[2] = 1
            if pp[1] == en[1]:
                self.action[2] = 0

            self.action[0] = 'идем'

