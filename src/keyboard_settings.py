import pygame

from settings import width, height, resolution, fps
from support import transformation
from Button import Button, KeyButtons

pygame.init()

font_name = 'font/custom/HOOG0554.TTF'
click_sound = '../sound/menu/click.mp3'


class KeyboardSettings:
    def __init__(self):
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("keyboard")

        title_font = pygame.font.Font(font_name, 70)
        self.title = title_font.render('keyboard', 1, '#000000')

        self.main_rect = pygame.Rect((width // 2 - 600, 130), (1200, 400))
        self.main_rect_color = '#D2D2D2'

        text_font = pygame.font.Font(font_name, 30)
        self.up_text = text_font.render('up:', 1, '#000000')
        self.down_text = text_font.render('down:', 1, '#000000')
        self.left_text = text_font.render('left:', 1, '#000000')
        self.right_text = text_font.render('right:', 1, '#000000')
        self.action_text = text_font.render('action:', 1, '#000000')

        self.dash_text = text_font.render('dash:', 1, '#000000')
        self.interface_text = text_font.render('interface:', 1, '#000000')
        # self.hotbar_text = text_font.render('hotbar:', 1, '#000000')
        self.console_text = text_font.render('console:', 1, '#000000')
        self.pause_text = text_font.render('pause:', 1, '#000000')

        self.text_list = [self.up_text, self.down_text, self.left_text, self.right_text,
                          self.action_text, self.dash_text, self.interface_text, self.console_text, self.pause_text]

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
                if self.key_bttns.num >= 0:
                    self.key_bttns.key_change(event.key)
                if event.key == pygame.K_ESCAPE:
                    transformation(self.surface)
                    self.running = False
            '''нажатие на кнопки'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.key_bttns.click(event.pos)
                self.ok_bttn.click(event.pos)
                self.exit_bttn.click(event.pos)
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                if self.ok_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.key_bttns.save()
                    self.running = False
                if self.exit_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.running = False
                self.key_bttns.no_click(event.pos)
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                self.ok_bttn.on_the_button(event.pos)
                self.exit_bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        pygame.draw.rect(self.surface, self.main_rect_color, self.main_rect, border_radius=10)
        self.surface.blit(self.title, (width // 2 - 200, 50))

        x, y = width // 2 - 500, 180
        for text in self.text_list[:5:]:
            self.surface.blit(text, (x, y))
            y += 70
        x, y = width // 2 + 50, 180
        for text in self.text_list[5::]:
            self.surface.blit(text, (x, y))
            y += 70

        self.key_bttns.draw()
        self.ok_bttn.draw()
        self.exit_bttn.draw()

        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = KeyboardSettings()
    menu.run()
