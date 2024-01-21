from main_menu import MainMenu
from settings import resolution

import pygame

if __name__ == '__main__':
    pygame.init()
    menu = MainMenu(pygame.display.set_mode(resolution))
    menu.run()
