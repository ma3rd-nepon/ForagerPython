import pygame
import sys

from game import Game
from settings import width, height, resolution, fps

pygame.init()
# resolution = width, height = 1296, 720
# fps = 60
font = pygame.font.Font('font/custom/HOOG0554.TTF', 30)


class Settings:
    def __init__(self):
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("settings")

        title_font = pygame.font.Font('font/custom/HOOG0554.TTF', 70)
        self.title = title_font.render('settings', 1, '#000000')

        self.exit_bttn = Button('exit', 300, 80,
                                (width // 2 - 150, height // 2 + 200), self.screen, 10)

        self.running = True

    def run(self):
        while self.running:
            # self.changing()
            # self.update()
            self.events()
        # pygame.display.quit()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.exit_bttn.click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.exit_bttn.no_click(event.pos):
                    self.running = False
                    menu.run()
            if event.type == pygame.MOUSEMOTION:
                self.exit_bttn.on_the_button(event.pos)
        self.screen.fill('#dcddd8')
        self.exit_bttn.draw()

        self.screen.blit(self.title, (width // 2 - 200, 200))
        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)


class Button:
    def __init__(self, text, w, h, coords, surface, scope):
        self.width = w
        self.height = h
        self.x, self.y = coords
        self.surface = surface
        self.original_scope = scope
        self.scope = scope

        self.upper_bttn = pygame.Rect(coords, (w, h))
        self.upper_color = '#A2AFB8'

        self.lower_bttn = pygame.Rect(coords, (w, scope))
        self.lower_color = '#5B6974'

        self.text = font.render(text, 1, '#FFFFFF')
        self.text_rect = self.text.get_rect(center=self.upper_bttn.center)

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


class Menu:
    def __init__(self, surface):
        # pygame.init()
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.running = True

        self.play_bttn = Button('play', 300, 80,
                                (width // 2 - 150, height // 2), self.surface, 10)
        self.settings_bttn = Button('settings', 300, 80,
                                    (width // 2 - 150, height // 2 + 100), self.surface, 10)
        self.exit_bttn = Button('exit', 300, 80,
                                (width // 2 - 150, height // 2 + 200), self.surface, 10)

        title_font = pygame.font.Font('font/custom/HOOG0554.TTF', 90)
        self.title = title_font.render('MENU', 1, '#000000')

    def run(self):
        while self.running:
            # self.changing()
            # self.update()
            self.events()
        # pygame.display.quit()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_bttn.click(event.pos)
                self.settings_bttn.click(event.pos)
                self.exit_bttn.click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_bttn.no_click(event.pos):
                    game = Game()
                    game.run()

                elif self.settings_bttn.no_click(event.pos):
                    settings = Settings()
                    settings.run()

                elif self.exit_bttn.no_click(event.pos):
                    self.running = False
            if event.type == pygame.MOUSEMOTION:
                self.play_bttn.on_the_button(event.pos)
                self.settings_bttn.on_the_button(event.pos)
                self.exit_bttn.on_the_button(event.pos)
        self.surface.fill('#dcddd8')
        self.play_bttn.draw()
        self.settings_bttn.draw()
        self.exit_bttn.draw()

        self.surface.blit(self.title, (width // 2 - 160, 200))
        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)


screen = pygame.display.set_mode(resolution)
menu = Menu(screen)
