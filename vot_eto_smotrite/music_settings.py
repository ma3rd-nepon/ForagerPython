import pygame

from settings import width, height, resolution, fps
from support import transformation
from Button import Button, KeyButtons

pygame.init()

font_name = 'font/custom/HOOG0554.TTF'
click_sound = '../sounds/menu_sounds/click.mp3'


class MusicSettings:
    def __init__(self):
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("music")

        title_font = pygame.font.Font(font_name, 70)
        self.title = title_font.render('music', 1, '#000000')

        # self.main_rect = pygame.Rect((width // 2 - 600, 130), (1200, 400))
        # self.main_rect_color = '#D2D2D2'

        self.key_bttns = KeyButtons(self.surface, click_sound)
        self.ok_bttn = Button('ok!', 300, 80,
                              (width // 2 - 310, height // 2 + 200), self.surface, 10, click_sound)
        self.exit_bttn = Button('exit', 300, 80,
                                (width // 2 + 10, height // 2 + 200), self.surface, 10, click_sound)

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
                self.ok_bttn.click(event.pos)
                self.exit_bttn.click(event.pos)
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                if self.ok_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.running = False
                if self.exit_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.running = False
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                self.ok_bttn.on_the_button(event.pos)
                self.exit_bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        self.surface.blit(self.title, (width // 2 - 200, 50))

        self.ok_bttn.draw()
        self.exit_bttn.draw()

        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = MusicSettings()
    menu.run()
