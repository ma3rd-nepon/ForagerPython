import random
import sprite_cut

from level import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, barrier_group):
        super().__init__()
        self.game = game
        self.barrier_sprites = barrier_group

        self.frames = sprite_cut.cut_sprite(ghost, 6, 2, 83, 87)
        self.cur_f = 0
        self.image = self.frames[0]
        self.current_image = self.image
        self.rect = self.image.get_rect()

        self.wmp = self.game.level.load_layer('map.csv')

        self.width, self.height = len(self.wmp[0]), len(self.wmp)

        self.x, self.y = None, None

        self.index = 0
        self.action = self.definit_action()

        self.flipx, self.flipy = False, False

        self.def_pos()

    def def_pos(self):
        """Определяет рандом позицию для врага """
        self.x, self.y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        if self.wmp[self.y][self.x] == '-1':
            self.rect.x = self.x * tilesize
            self.rect.y = self.y * tilesize
            return
        self.def_pos()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.flip()
        self.animate_idle()

    def move(self):
        """Движение врага"""
        cof = 2
        if self.action[0] == 'стоим':
            self.index += 1
            if self.index >= 60:
                self.index = 0
                self.action = self.definit_action()

        if self.action[0] == 'идем':
            self.index += 2
            if self.index == 60:
                self.index = 0
                self.action = self.definit_action()

            self.rect.x += cof * self.action[1]
            self.collision('x')
            self.rect.y += cof * self.action[2]
            self.collision('y')

    def definit_action(self):
        """Определение действия врага (идти или стоять)"""
        return [random.choice(['идем', 'стоим']), random.randint(-1, 1), random.randint(-1, 1)]

    def flip(self):
        """Поворот в сторону движения"""
        if self.action[1] == -1:
            self.flipx = True
        elif self.action[1] == 1:
            self.flipx = False
    
    def collision(self, direct):
        """Коллизия с обьектами"""
        for sprite in self.barrier_sprites:
            if sprite.rect.colliderect(self.rect):
                if direct == 'x':
                    if self.action[1] == -1:  # враг шел влево
                        self.rect.left = sprite.rect.right
                    if self.action[1] == 1:  # враг шел вправо
                        self.rect.right = sprite.rect.left

                if direct == 'y':
                    if self.action[2] == -1:  # враг шел вверх
                        self.rect.top = sprite.rect.bottom
                    if self.action[2] == 1:  # враг шел вниз
                        self.rect.bottom = sprite.rect.top

    def enemy_on_screen(self):
        """Проверить есть ли враг на экране"""
        eom = (self.rect.x // tilesize, self.rect.y // tilesize)
        pom = self.game.plyr.player_on_map()
        if all([pom[0] - 8 <= eom[0] <= pom[0] + 8, pom[1] - 5 <= eom[1] <= pom[1] + 5]):
            return True
        return False

    def animate_idle(self):
        """Анимация врага"""
        self.cur_f += 0.2

        if self.cur_f >= len(self.frames):
            self.cur_f = 0

        self.current_image = self.frames[int(self.cur_f)]
        self.image = pygame.transform.flip(self.current_image, self.flipx, self.flipy)
