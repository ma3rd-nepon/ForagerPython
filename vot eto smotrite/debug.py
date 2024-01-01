import pygame

from settings import *

pygame.init()
font = pygame.font.Font(None, 30)


def debug(*args, y=height-30, x=10):
    screen = pygame.display.get_surface()
    info = f'{[a for a in args]}'
    debug_scr = font.render(info, True, 'white')
    debug_rect = debug_scr.get_rect()
    pygame.draw.rect(screen, 'black', debug_rect)

    screen.blit(debug_scr, debug_rect)

