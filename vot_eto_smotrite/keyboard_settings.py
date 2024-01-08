import pygame

from settings import width, height, resolution, fps
from support import transformation
from Button import Button

pygame.init()

font_name = 'font/custom/HOOG0554.TTF'
click_sound = '../sounds/menu_sounds/click.mp3'


# background2 = pygame.image.load('../sprites/menu/background2.png')


class KeyboardSettings:
    def __init__(self):
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("keyboard")

        title_font = pygame.font.Font(font_name, 70)
        self.title = title_font.render('settings', 1, '#000000')

        self.rect = pygame.Rect((width // 2 - 550, 130), (1100, 420))
        self.rect_color = '#D2D2D2'

        text_font = pygame.font.Font(font_name, 30)
        self.up_text = text_font.render('up:', 1, '#000000')
        self.down_text = text_font.render('down:', 1, '#000000')
        self.left_text = text_font.render('left:', 1, '#000000')
        self.right_text = text_font.render('right:', 1, '#000000')
        self.action_text = text_font.render('action:', 1, '#000000')
        self.inventory_text = text_font.render('inventory:', 1, '#000000')
        self.pause_text = text_font.render('pause:', 1, '#000000')

        self.text_list = [self.up_text, self.down_text, self.left_text, self.right_text,
                          self.action_text, self.inventory_text, self.pause_text]
        self.ok_bttn = Button('ok!', 300, 80,
                              (width // 2 - 150, height // 2 + 220), self.surface, 10, click_sound)
        # self.keyboard_bttn = Button('keyboard', 300, 80,
        #                             (width // 2 - 150, height // 2 + 100), self.surface, 10, click_sound)
        # self.music_bttn = Button('music', 300, 80,
        #                          (width // 2 - 150, height // 2), self.surface, 10, click_sound)
        #
        # self.buttons_list = [self.music_bttn, self.keyboard_bttn, self.exit_bttn]

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
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                self.ok_bttn.no_click(event.pos)
                transformation(self.surface)
                self.running = False
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                self.ok_bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        pygame.draw.rect(self.surface, self.rect_color, self.rect, border_radius=10)
        self.surface.blit(self.title, (width // 2 - 200, 50))

        x, y = width // 2 - 500, 180
        for text in self.text_list:
            self.surface.blit(text, (x, y))
            y += 50

        self.ok_bttn.draw()
        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = KeyboardSettings()
    menu.run()
