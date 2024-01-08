import pygame

from settings import width

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
        self.button_rect_color = '#5B5C5E'
        if sound:
            self.sound = pygame.mixer.Sound(sound)

        x, y = width // 2 - 200, 160
        for _ in range(5):
            self.key_bttns_list.append(pygame.Rect((x, y), (50, 50)))
            y += 71

        x, y = width // 2 + 450, 160
        for _ in range(5):
            self.key_bttns_list.append(pygame.Rect((x, y), (50, 50)))
            y += 71
        # print(self.key_bttns_list)

    def draw(self):
        for button in self.key_bttns_list:
            pygame.draw.rect(self.surface, self.button_rect_color, button, border_radius=10)

    def click(self, pos):
        for num, button in enumerate(self.key_bttns_list):
            if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                self.button_rect_color = '#5B5C5E'
                if self.sound:
                    self.sound.play()
                print(num + 1)

    def no_click(self, pos):
        for num, button in enumerate(self.key_bttns_list):
            if (button.x <= pos[0] <= button.width + button.x) and (button.y <= pos[1] <= button.height + button.y):
                pass
                # self.button_rect_color = '#406500'
            #     return True
            # return False