import pygame

from settings import width, height, resolution, fps
from support import transformation
from Button import Button
from keyboard_settings import KeyboardSettings

pygame.init()

font = pygame.font.Font('font/custom/HOOG0554.TTF', 30)
click_sound = '../sounds/menu_sounds/click.mp3'


# background2 = pygame.image.load('../sprites/menu/background2.png')


class Settings:
    def __init__(self):
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("settings")

        title_font = pygame.font.Font('font/custom/HOOG0554.TTF', 70)
        self.title = title_font.render('settings', 1, '#000000')

        self.exit_bttn = Button('exit', 300, 80,
                                (width // 2 - 150, height // 2 + 200), self.surface, 10, click_sound)
        self.keyboard_bttn = Button('keyboard', 300, 80,
                                    (width // 2 - 150, height // 2 + 100), self.surface, 10, click_sound)
        self.music_bttn = Button('music', 300, 80,
                                 (width // 2 - 150, height // 2), self.surface, 10, click_sound)

        self.buttons_list = [self.music_bttn, self.keyboard_bttn, self.exit_bttn]

        self.running = True

    def run(self):
        while self.running:
            self.update()
            self.events()

    def events(self):
        for event in pygame.event.get():
            '''выход'''
            if event.type == pygame.QUIT:
                transformation(self.surface)
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transformation(self.surface)
                    self.running = False
            '''нажатие на кнопки'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bttn in self.buttons_list:
                    bttn.click(event.pos)
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                if self.exit_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.running = False
                if self.keyboard_bttn.no_click(event.pos):
                    transformation(self.surface)
                    keyboard = KeyboardSettings()
                    keyboard.run()
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                for bttn in self.buttons_list:
                    bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        # self.surface.blit(background2, (0, 0))
        for bttn in self.buttons_list:
            bttn.draw()

        self.surface.blit(self.title, (width // 2 - 200, 50))
        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)