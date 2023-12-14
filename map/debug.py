import pygame

from settings import *

pygame.init()
font = pygame.font.Font(None, 30)


def debug(fps, speed, y=h-30, x=10):
    screen = pygame.display.get_surface()
    info = f'{fps :.1f}         [{speed[0] :.4f}, {speed[1] :.4f}]'
    debug_scr = font.render(info, True, 'white')
    debug_rect = debug_scr.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, 'black', debug_rect)

    screen.blit(debug_scr, debug_rect)

