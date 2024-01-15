from game import Game
from menu import Menu
# from game import Game
from main_menu import MainMenu
from settings import resolution

import pygame

if __name__ == '__main__':
    pygame.init()
    menu = Menu(pygame.display.set_mode(resolution))
    game = Game()
    # game = Game()
    menu = MainMenu(pygame.display.set_mode(resolution))
    menu.run()
    game.run()
    # game.run()

# da
