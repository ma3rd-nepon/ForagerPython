import sys
import pygame

from settings import width, height, resolution, fps
from Button import Button
from settings_menu import Settings
from main import Game

pygame.init()
# resolution = width, height = 1296, 720
# fps = 60
font = pygame.font.Font('font/custom/HOOG0554.TTF', 30)


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


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = Menu(screen)
    menu.run()
