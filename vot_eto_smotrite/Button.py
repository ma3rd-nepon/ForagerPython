import pygame


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
        self.upper_color = '#A2AFB8'

        self.lower_bttn = pygame.Rect(coords, (w, scope))
        self.lower_color = '#5B6974'

        self.text = font.render(text, 1, '#FFFFFF')
        self.text_rect = self.text.get_rect(center=self.upper_bttn.center)
        if sound:
            self.sound = pygame.mixer.Sound(sound)

        self.pressed = False

    def draw(self):
        self.upper_bttn.y = self.y - self.scope  # тут положение кнопки изменяется
        self.text_rect.center = self.upper_bttn.center  # тут текст за центром кнопки катается

        self.lower_bttn.midtop = self.upper_bttn.midtop
        self.lower_bttn.height = self.upper_bttn.height + self.scope

        pygame.draw.rect(self.surface, self.lower_color, self.lower_bttn, border_radius=20)
        pygame.draw.rect(self.surface, self.upper_color, self.upper_bttn, border_radius=20)
        self.surface.blit(self.text, self.text_rect)

    def click(self, pos):
        if (self.x <= pos[0] <= self.width + self.x) and (self.y <= pos[1] <= self.height + self.y):
            self.pressed = True
            self.scope = 0

    def no_click(self, pos):
        if (self.x <= pos[0] <= self.width + self.x) and (self.y <= pos[1] <= self.height + self.y):
            self.pressed = False
            self.scope = self.original_scope
            if self.sound:
                self.sound.play()
            return True
        return False

    def on_the_button(self, pos):
        if ((self.x <= pos[0] <= self.width + self.x)
                and (self.y <= pos[1] <= self.height + self.y)):
            self.upper_color = '#90D71D'
        else:
            self.scope = self.original_scope  # можно и убрать
            self.upper_color = '#A2AFB8'

    def debug(self):
        print(self.pressed)
