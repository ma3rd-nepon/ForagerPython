from settings import *

pygame.init()


class FinishWind:
    def __init__(self, surface, statement, cool_image, sound, attempt, days, resources, wins):
        self.surface = surface
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        self.statement = statement
        self.attempt = attempt
        self.days = days
        self.resources = resources
        self.wins = wins
        self.end_sound = pygame.mixer.Sound(sound)

        self.title_font = pygame.font.Font('font/custom/HOOG0554.TTF', 70)
        self.descr_font = pygame.font.Font('font/custom/HOOG0554.TTF', 30)
        self.main_rect = pygame.Rect((width // 2 - 450, 100), (900, 500))

        self.cat_image = pygame.image.load(cool_image)
        self.cat_w = self.cat_image.get_width()
        self.check = 0
        self.running = True

    def run(self):
        chanel4.play(self.end_sound)
        while self.running:
            self.update()
            self.events()

    def events(self):
        # я специально никак не задействую нажатие на крестик!!!
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.check = 0
                if event.key == pygame.K_RSHIFT:
                    self.check = 1 if self.check == 0 else 0

    def update(self):
        if self.check == 0:
            self.check_info()
        else:
            self.check_res()
        pygame.display.update()
        self.clock.tick(fps)

    def check_res(self):
        title = self.title_font.render('results', 1, '#000000')
        title_w = title.get_width()
        cat_image = pygame.image.load('../sprites/menu/cat2.png')

        results = (
            self.descr_font.render(f'day {self.days}', 1, '#000000'),
            self.descr_font.render(f'number of resources - {self.resources}', 1, '#000000'),
            self.descr_font.render(f'total number of attempts - {self.attempt}', 1, '#000000'),
            self.descr_font.render(f'total number of wins - {self.wins}', 1, '#000000')
        )

        pygame.draw.rect(self.surface, '#FFFFFF', self.main_rect, border_radius=10)
        self.surface.blit(title, (width // 2 - (title_w // 2), 130))
        self.surface.blit(cat_image, (width // 2 + 150, 355))
        y = 220
        for result in results:
            self.surface.blit(result, (width // 2 - 400, y))
            y += 50

    def check_info(self):
        title = self.title_font.render(self.statement, 1, '#000000')
        title_w = title.get_width()
        description1 = self.descr_font.render('press space to start again', 1, '#000000')
        descr1_w = description1.get_width()
        description2 = self.descr_font.render('press escape to return to the menu', 1, '#000000')
        descr2_w = description2.get_width()
        description3 = self.descr_font.render('press rightshift to see results', 1, '#000000')
        descr3_w = description3.get_width()

        pygame.draw.rect(self.surface, '#FFFFFF', self.main_rect, border_radius=10)
        self.surface.blit(title, (width // 2 - (title_w // 2), 130))
        self.surface.blit(description1, (width // 2 - (descr1_w // 2), 210))
        self.surface.blit(description2, (width // 2 - (descr2_w // 2), 260))
        self.surface.blit(description3, (width // 2 - (descr3_w // 2), 310))
        self.surface.blit(self.cat_image, (width // 2 - (self.cat_w // 2), 350))


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    menu = FinishWind(pygame.display.set_mode(resolution), 'good job',
                      '../sprites/menu/ourbro.png', '../sound/game/win.mp3',
                      2, 2, 14, 10)
    menu.run()
