import pygame


class PLayer(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../1-level/graphics/test/player.png').convert_alpha()
        self.rect = self.get_rect(topleft=pos)
