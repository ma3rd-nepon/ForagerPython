import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):
    screen = pygame.display.get_surface()
    debug_scr = font.render(str(info), True, 'white')
    debug_rect = debug_scr.get_rect(topleft = (x, y))
    pygame.draw.rect(screen, 'black', debug_rect)
    screen.blit(debug_scr, debug_rect)

