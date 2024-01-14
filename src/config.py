import pygame

with open('keyboard.txt') as file:
    keys = [(x.rstrip().rsplit(' ', 1)) for x in file.readlines()[:9:] if x]

move = up, left, down, right = (eval(f'pygame.{keys[0][1]}'), eval(f'pygame.{keys[2][1]}'),
                                eval(f'pygame.{keys[1][1]}'), eval(f'pygame.{keys[3][1]}'))

hit = eval(f'pygame.{keys[4][1]}')

dash = eval(f'pygame.{keys[5][1]}')

hide_hud = eval(f'pygame.{keys[6][1]}')

console = eval(f'pygame.{keys[7][1]}')

pause = eval(f'pygame.{keys[8][1]}')

skip_title = 13  # enter

hotbar = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

inventory = 9


with open('sounds_value.txt') as file:
    sound_values = [x.rstrip() for x in file.readlines() if x]

menu_mus_val = float(sound_values[0])
game_mus_val = float(sound_values[1])
sound_ef_val = float(sound_values[2])
