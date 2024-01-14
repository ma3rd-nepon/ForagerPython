# from game import Game
from main_menu import MainMenu
from settings import resolution

import pygame

if __name__ == '__main__':
    pygame.init()
    # game = Game()
    menu = MainMenu(pygame.display.set_mode(resolution))
    menu.run()
    # game.run()

# da
