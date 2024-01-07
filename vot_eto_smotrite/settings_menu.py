import sys
import pygame

from settings import width, height, resolution, fps
from main_menu import Menu
from Button import Button

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
                    menu = Menu(self.screen)
                    menu.run()
            if event.type == pygame.MOUSEMOTION:
                self.exit_bttn.on_the_button(event.pos)
        self.screen.fill('#dcddd8')
        self.exit_bttn.draw()

        self.screen.blit(self.title, (width // 2 - 200, 200))
        # pygame.display.flip()
        pygame.display.update()
        self.clock.tick(fps)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = Menu(screen)
    menu.run()
