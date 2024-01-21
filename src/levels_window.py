import sys

from settings import *
from support import transformation
from Button import Button
from game import Game
from config import Configuration

pygame.init()
# font = pygame.font.Font('../src/font/custom/HOOG0554.TTF', 30)
click_sound = '../sound/menu/click.mp3'
back_music = '../sound/menu/background.wav'
background1 = pygame.image.load('../sprites/menu/game_title.png')


class LevelsMenu:
    def __init__(self):
        # pygame.init()
        pygame.display.set_caption('levels menu')
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(resolution)
        self.running = True

        self.easy_bttn = Button('easy', 250, 80,
                                (width // 2 - 535, height // 2 + 50), self.surface, 10, click_sound)
        self.medium_bttn = Button('medium', 250, 80,
                                  (width // 2 - 100, height // 2 + 50), self.surface, 10, click_sound)
        self.hard_bttn = Button('hard', 250, 80,
                                (width // 2 + 305, height // 2 + 50), self.surface, 10, click_sound)
        self.buttons_list = [self.easy_bttn, self.medium_bttn, self.hard_bttn]

        title_font = pygame.font.Font('../src/font/custom/HOOG0554.TTF', 70)
        self.title = title_font.render('choose level', 1, '#000000')
        self.title_w = self.title.get_width()

        self.config = Configuration()
        self.menu_mus_val = self.config.menu_mus_val

        self.menu_music = pygame.mixer.Sound(back_music)
        self.menu_music.set_volume(self.menu_mus_val)

    def run(self):
        while self.running:
            self.update()
            self.events()

    def events(self):
        for event in pygame.event.get():
            '''выход'''
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            '''нажатие на кнопки'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bttn in self.buttons_list:
                    bttn.click(event.pos)
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                if self.easy_bttn.no_click(event.pos):
                    transformation(self.surface)
                    chanel3.pause()
                    game = Game(200, 5, 2, 100)
                    game.run()
                elif self.medium_bttn.no_click(event.pos):
                    transformation(self.surface)
                    chanel3.pause()
                    game = Game(150, 7, 3, 150)
                    game.run()
                elif self.hard_bttn.no_click(event.pos):
                    transformation(self.surface)
                    chanel3.pause()
                    game = Game(100, 8, 4, 150)
                    game.run()
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                for bttn in self.buttons_list:
                    bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        # self.surface.blit(background1, (0, 0))
        for bttn in self.buttons_list:
            bttn.draw()
        self.surface.blit(self.title, (width // 2 - (self.title_w // 2), 50))
        self.config.update_values()
        self.menu_mus_val = self.config.menu_mus_val
        self.menu_music.set_volume(self.menu_mus_val)
        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = LevelsMenu()
    menu.run()
