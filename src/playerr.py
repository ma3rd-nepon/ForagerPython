import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, barrier_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../1-level/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.barrier_sprites = barrier_sprites

        self.movement()

    def movement(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.y = 1
        elif key[pygame.K_a]:
            self.direction.x = -1
        elif key[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.y = 0

        if key[pygame.K_a]:
            self.direction.x = -1
        elif key[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def collision(self, direction):
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

    def moving(self, speed):
        if self.direction.magnitude() != 0:  # длина вектора
            self.direction = self.direction.normalize()  # деаем его длину = 1
        self.rect.x += self.direction.x * speed
        self.collision('горизонтально')
        self.rect.y += self.direction.y * speed
        self.collision('вертикально')
        # self.rect.center += self.direction * speed

    def update(self):
        self.movement()
        self.moving(self.speed)
