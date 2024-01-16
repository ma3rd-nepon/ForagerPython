import pygame

from settings import width, height, resolution, fps
from support import transformation
from Button import Button, KeyButtons, Slider
from config import Configuration

pygame.init()

font_name = 'font/custom/HOOG0554.TTF'
click_sound = '../sound/menu/click.mp3'


class MusicSettings:
    def __init__(self):
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("music")

        title_font = pygame.font.Font(font_name, 70)
        self.title = title_font.render('music', 1, '#000000')

        self.main_rect = pygame.Rect((width // 2 - 600, 130), (1200, 400))
        self.main_rect_color = '#D2D2D2'

        text_font = pygame.font.Font(font_name, 30)
        self.menu_mus_text = text_font.render('menu background music:', 1, '#000000')
        self.game_mus_text = text_font.render('game background music:', 1, '#000000')
        self.sound_ef_text = text_font.render('sound effects:', 1, '#000000')
        self.text_list = [self.menu_mus_text, self.game_mus_text, self.sound_ef_text]

        self.config = Configuration()
        sound_ef_val, menu_mus_val, game_mus_val = (self.config.sound_ef_val,
                                                    self.config.menu_mus_val, self.config.game_mus_val)

        self.key_bttns = KeyButtons(self.surface, click_sound)

        self.ok_bttn = Button('ok!', 300, 80,
                              (width // 2 - 310, height // 2 + 200), self.surface, 10, click_sound)
        self.exit_bttn = Button('exit', 300, 80,
                                (width // 2 + 10, height // 2 + 200), self.surface, 10, click_sound)

        self.menu_music_slider = Slider(300, 50, (width // 2 + 300, height // 2 - 135),
                                        self.surface, menu_mus_val, 0, 100)
        self.game_music_slider = Slider(300, 50, (width // 2 + 300, height // 2 - 35),
                                        self.surface, game_mus_val, 0, 100)
        self.sound_eff_slider = Slider(300, 50, (width // 2 + 300, height // 2 + 65),
                                       self.surface, sound_ef_val, 0, 100)

        self.sliders_list = [self.menu_music_slider, self.game_music_slider, self.sound_eff_slider]

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
                    self.save()
                    self.running = False
                if self.exit_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.running = False
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                self.ok_bttn.on_the_button(event.pos)
                self.exit_bttn.on_the_button(event.pos)

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                for slider in self.sliders_list:
                    slider.move_slider(event.pos)

    def save(self):
        sound_values = []
        for slider in self.sliders_list:
            sound_values.append(slider.get_value())

        with open('sounds_value.txt', 'w') as file:
            for val in sound_values:
                file.write(f'{val}\n')
        self.config.update_values()
        # MainMenu().menu_mus_val = self.config.menu_mus_val


    def update(self):
        self.surface.fill('#FFFFFF')
        pygame.draw.rect(self.surface, self.main_rect_color, self.main_rect, border_radius=10)
        self.surface.blit(self.title, (width // 2 - 150, 50))

        for slider in self.sliders_list:
            slider.draw()

        x, y = width // 2 - 500, 215
        for text in self.text_list:
            self.surface.blit(text, (x, y))
            y += 100

        self.ok_bttn.draw()
        self.exit_bttn.draw()

        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = MusicSettings()
    menu.run()
