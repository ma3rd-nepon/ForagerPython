from game import Game
from menu import Menu
from settings import resolution

import pygame

if __name__ == '__main__':
    pygame.init()
    menu = Menu(pygame.display.set_mode(resolution))
    game = Game()
    menu.run()
    game.run()

# da
