import pygame

dash = pygame.K_SPACE

console = pygame.K_BACKSLASH

skip_title = 13  # enter

hide_hud = pygame.K_F1

pause = pygame.K_ESCAPE

move = up, left, down, right = pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d

hit = pygame.K_n

hotbar = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

inventory = 9  # tab


with open('sounds_value.txt') as file:
    sound_values = [x.rstrip() for x in file.readlines() if x]

menu_mus_val = float(sound_values[0])
game_mus_val = float(sound_values[1])
sound_ef_val = float(sound_values[2])
