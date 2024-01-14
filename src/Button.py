import pygame

from settings import width, ALL_KEYS

pygame.init()
font = pygame.font.Font('font/custom/HOOG0554.TTF', 30)


class Button:
    def __init__(self, text, w, h, coords, surface, scope, sound=None):
        self.width = w
        self.height = h
        self.x, self.y = coords
        self.surface = surface
        self.sound = sound
        self.original_scope = scope
        self.scope = scope

        self.upper_bttn = pygame.Rect(coords, (w, h))
        self.upper_color = '#D2D2D2'

        self.lower_bttn = pygame.Rect(coords, (w, scope))
        self.lower_color = '#5B5C5E'

        self.text = font.render(text, 1, '#000000')
        self.text_rect = self.text.get_rect(center=self.upper_bttn.center)
        if sound:
            self.sound = pygame.mixer.Sound(sound)

        self.pressed = False

    def draw(self):
        self.upper_bttn.y = self.y - self.scope  # тут положение кнопки изменяется
        self.text_rect.center = self.upper_bttn.center  # тут текст за центром кнопки катается

        self.lower_bttn.midtop = self.upper_bttn.midtop
        self.lower_bttn.height = self.upper_bttn.height + self.scope

        pygame.draw.rect(self.surface, self.lower_color, self.lower_bttn, border_radius=10)
        pygame.draw.rect(self.surface, self.upper_color, self.upper_bttn, border_radius=10)
        self.surface.blit(self.text, self.text_rect)

    def click(self, pos):
        if (self.x <= pos[0] <= self.width + self.x) and (self.y <= pos[1] <= self.height + self.y):
            if self.sound:
                self.sound.play()
            self.pressed = True
            self.scope = 0

    def no_click(self, pos):
        if (self.x <= pos[0] <= self.width + self.x) and (self.y <= pos[1] <= self.height + self.y):
            self.pressed = False
            self.scope = self.original_scope
            return True
        return False

    def on_the_button(self, pos):
        if ((self.x <= pos[0] <= self.width + self.x)
                and (self.y <= pos[1] <= self.height + self.y)):
            self.upper_color = '#90D71D'
        else:
            self.scope = self.original_scope  # можно и убрать
            self.upper_color = '#D2D2D2'

    def debug(self):
        print(self.pressed)


class KeyButtons:
    def __init__(self, surface, sound=None):
        self.surface = surface
        self.key_bttns_list = []
        self.key_text_list = []
        self.keyboard = []
        self.button_rect_color = '#5B5C5E'
        self.num = -1
        self.colored = False
        if sound:
            self.sound = pygame.mixer.Sound(sound)

        x, y = width // 2 - 270, 160
        for _ in range(5):
            self.key_bttns_list.append(pygame.Rect((x, y), (170, 50)))
            y += 71

        x, y = width // 2 + 350, 160
        for _ in range(4):
            self.key_bttns_list.append(pygame.Rect((x, y), (170, 50)))
            y += 71
        self.get_keys_text()
        self.update_keys()

    def get_keys_text(self):
        with open('keyboard.txt', 'r') as file:
            self.keyboard = [(x.rstrip().rsplit(' ', 1)) for x in file.readlines()[:9:] if x]

    def update_keys(self):
        key_font = pygame.font.Font('font/custom/HOOG0554.TTF', 20)
        for num, button in enumerate(self.key_bttns_list):
            text = key_font.render(self.keyboard[num][1].split('_')[1].upper(), 1, '#FFFFFF')
            text_rect = text.get_rect(center=button.center)
            self.key_text_list.append((text, text_rect))

    def draw(self):
        self.update_keys()
        for num, button in enumerate(self.key_bttns_list):
            if self.num == num:
                pygame.draw.rect(self.surface, '#5F9600', button, border_radius=10)
            else:
                pygame.draw.rect(self.surface, self.button_rect_color, button, border_radius=10)
        for text_params in self.key_text_list:
            self.surface.blit(text_params[0], text_params[1])

    def click(self, pos):
        if self.num >= 0:
            button = self.key_bttns_list[self.num]
            if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                if self.sound:
                    self.sound.play()
        else:
            for num, button in enumerate(self.key_bttns_list):
                if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                    if self.sound:
                        self.sound.play()

    def key_change(self, event):
        for key in ALL_KEYS:
            if event == eval(f'pygame.{key}'):
                self.keyboard[self.num][1] = str(key)
        self.key_text_list = []

    def no_click(self, pos):
        if self.num == -1:
            for num, button in enumerate(self.key_bttns_list):
                if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                    if not self.colored:
                        self.num = num
                        self.colored = True
                    else:
                        self.num = -1
                        self.colored = False
        else:
            button = self.key_bttns_list[self.num]
            if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                self.num = -1
                self.colored = False

    def save(self):
        with open('keyboard.txt', 'w') as file:
            for row in self.keyboard:
                file.write(f'{row[0]} {row[1]}\n')
