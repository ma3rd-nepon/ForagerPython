import sys
import pygame

from settings import width, height, fps
from support import transformation
from Button import Button
from settings_menu import Settings
from game import Game
from config import Configuration

pygame.init()
font = pygame.font.Font('../src/font/custom/HOOG0554.TTF', 30)
click_sound = '../sound/menu/click.mp3'
back_music = '../sound/menu/background.wav'
background1 = pygame.image.load('../sprites/menu/game_title.png')


class MainMenu:
    def __init__(self, surface):
        # pygame.init()
        pygame.display.set_caption('main menu')
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.running = True

        self.play_bttn = Button('play', 250, 80,
                                (width // 2 - 535, height // 2 + 200), self.surface, 10, click_sound)
        self.settings_bttn = Button('settings', 250, 80,
                                    (width // 2 - 255, height // 2 + 200), self.surface, 10, click_sound)
        self.support_bttn = Button('support', 250, 80,
                                   (width // 2 + 25, height // 2 + 200), self.surface, 10, click_sound)

        self.exit_bttn = Button('exit', 250, 80,
                                (width // 2 + 305, height // 2 + 200), self.surface, 10, click_sound)
        self.buttons_list = [self.play_bttn, self.settings_bttn, self.exit_bttn, self.support_bttn]

        self.config = Configuration()
        self.menu_mus_val = self.config.menu_mus_val

        self.menu_music = pygame.mixer.Sound(back_music)
        self.menu_music.set_volume(self.menu_mus_val)
        # self.menu_music.play(loops= -1)
        # title_font = pygame.font.Font('font/custom/HOOG0554.TTF', 90)
        # self.title = title_font.render('menu', 1, '#000000')

    def run(self):
        self.menu_music.play(loops=-1)
        while self.running:
            # self.music.play()
            self.update()
            self.events()
            # self.menu_music.play(loops=-1)
        # pygame.display.quit()
        pygame.quit()
        sys.exit()

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
                if self.play_bttn.no_click(event.pos):
                    transformation(self.surface)
                    self.menu_music.stop()
                    game = Game()
                    game.run()
                elif self.settings_bttn.no_click(event.pos):
                    transformation(self.surface)
                    settings = Settings()
                    settings.run()
                elif self.exit_bttn.no_click(event.pos):
                    self.running = False
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                for bttn in self.buttons_list:
                    bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        self.surface.blit(background1, (0, 0))
        for bttn in self.buttons_list:
            bttn.draw()
        # self.surface.blit(self.title, (width // 2 - 160, 200))
        self.config.update_values()
        self.menu_mus_val = self.config.menu_mus_val
        self.menu_music.set_volume(self.menu_mus_val)
        pygame.display.update()
        self.clock.tick(fps)


# if __name__ == '__main__':
#     screen = pygame.display.set_mode(resolution)
#     menu = MainMenu(screen)
#     menu.run()
