import pygame


class Configuration:
    def __init__(self):
        self.menu_mus_val, self.game_mus_val, self.sound_ef_val = None, None, None
        self.move = self.up, self.left, self.down, self.right = None, None, None, None
        self.hit, self.dash, self.hide_hud, self.console, self.pause = None, None, None, None, None
        self.skip_title = 13  # enter
        self.hotbar = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
        self.inventory = 9
        self.update_values()

    def update_values(self):
        with open('sounds_value.txt') as file:
            sound_values = [x.rstrip() for x in file.readlines() if x]

        with open('keyboard.txt') as file:
            keys = [(x.rstrip().rsplit(' ', 1)) for x in file.readlines()[:9:] if x]

        self.menu_mus_val = float(sound_values[0])
        self.game_mus_val = float(sound_values[1])
        self.sound_ef_val = float(sound_values[2])

        self.move = self.up, self.left, self.down, self.right = \
            (eval(f'pygame.{keys[0][1]}'), eval(f'pygame.{keys[2][1]}'),
             eval(f'pygame.{keys[1][1]}'), eval(f'pygame.{keys[3][1]}'))
        self.hit = eval(f'pygame.{keys[4][1]}')
        self.dash = eval(f'pygame.{keys[5][1]}')
        self.hide_hud = eval(f'pygame.{keys[6][1]}')
        self.console = eval(f'pygame.{keys[7][1]}')
        self.pause = eval(f'pygame.{keys[8][1]}')
