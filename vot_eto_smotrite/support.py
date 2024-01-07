import pygame
from settings import resolution

pygame.init()


def transformation(screen):
    running = True
    alpha = 0
    while running:
        for event in pygame.event.get():
            '''выход'''
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        surface = pygame.Surface(resolution)
        surface.fill((0, 0, 0))
        surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))

        alpha += 5
        if alpha >= 255:
            alpha = 255
            running = False

        pygame.display.flip()
