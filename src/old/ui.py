from settings import *
from imgs import *


class Player_UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.font.init()
        self.game = game

        self.pause_ui = pygame.Surface((width, height), pygame.SRCALPHA)

        self.title_scrn = pygame.Surface((width, height), pygame.SRCALPHA)

        self.hotbar_scr = pygame.Surface((width, height), pygame.SRCALPHA)

        self.coin_image = pygame.transform.rotozoom(coin.convert_alpha(), 0, 0.5)

        self.heart_image = pygame.transform.rotozoom(heart.convert_alpha(), 0, 0.35)
        self.heart_image2 = self.heart_image
        self.heart_image3 = self.heart_image

        self.heart_hb = self.heart_image.get_rect()
        self.heart2_hb = self.heart_image2.get_rect()
        self.heart3_hb = self.heart_image3.get_rect()
        self.coin_hb = self.coin_image.get_rect()

        self.heart_hb.x, self.heart_hb.y = 10, 10
        self.heart2_hb.x, self.heart2_hb.y = 48, 10
        self.heart3_hb.x, self.heart3_hb.y = 86, 10
        self.coin_hb.x, self.coin_hb.y = 20, height - 70

        self.coin_count = 0  # колво монет
        self.coin_font = pygame.font.Font(font, 40)  # шрифт для цифры
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False,
                                                     'white', 'black')  # рендер текста

        self.fps_font = pygame.font.Font(font, 20)
        self.fps = self.fps_font.render(f"{self.game.clock.get_fps()}", False, 'white', 'black')

        # crosshair
        self.cross_im = crosshair
        self.cross = self.cross_im.get_rect()

        # energy bar
        self.percentage = 100

        # timer
        self.time = [12, 0]
        self.imdxxx = 0

        self.hb_things = []

        self.key = pygame.key.get_pressed()

        self.show_hud = False

        self.title_index = 0

    def draw(self):
        """Отрисовка всех элементов интерфейса"""
        self.game.screen.blit(self.heart_image, self.heart_hb)
        self.game.screen.blit(self.heart_image2, self.heart2_hb)
        self.game.screen.blit(self.heart_image3, self.heart3_hb)

        self.game.screen.blit(self.coin_image, self.coin_hb)
        self.game.screen.blit(self.coin_count_text, (90, height - 55))

        self.game.screen.blit(self.fps, (width - 35, 10))

        self.game.screen.blit(self.hotbar_scr, (0, 0))

        self.draw_energy(self.percentage)

        self.draw_timer()

        self.draw_crosshair(False)

        self.draw_hotbar()

    def update(self):
        """Обновление интерфейса"""
        if self.game.game and not self.game.pause:
            if self.coin_count > 10000:
                self.coin_count = 10000

            self.coin_count_text = self.coin_font.render(str(self.coin_count), False, 'white', 'black')
            self.fps = self.fps_font.render(f"{int(self.game.clock.get_fps())}", False, 'white', 'black')

            if self.show_hud:
                self.draw()

            self.imdxxx += 0.3  # скорость течения времени ( игровая минута != секунда реальная)
            if int(self.imdxxx) == 60:
                self.imdxxx = 0
                self.time[1] += 1

            if self.time[1] == 60:
                self.time[1] = 0
                self.time[0] += 1
                self.imdxxx = 0
                if self.time[0] == 24:
                    self.time[0] = 0

        if not self.game.game:
            self.game.screen.blit(self.title_scrn, (0, 0))

    def draw_energy(self, percent: int):
        """Отрисовка полоски энергии"""
        perc = float(percent / 100)
        if perc < 0:
            perc = 0
        pygame.draw.rect(self.game.screen, 'black', (10, 60, 105, 30))
        pygame.draw.rect(self.game.screen, '#90EE90', (15, 65, 95 * perc, 20))

    def draw_timer(self):
        """Отображает игровое время"""
        timee = self.fps_font.render(f"{self.time[0]}:{str(self.time[1])}", False, 'white', 'black')
        self.game.screen.blit(timee, (width - 80, 40))

    def pause(self):
        if self.game.pause:
            self.pause_ui.fill((0, 0, 0, 100), (0, 0, width, height))
            name = self.coin_font.render('test pause', False, 'white')
            self.pause_ui.blit(name, ((width / 2) - 170, 20))
            self.game.screen.blit(self.pause_ui, (0, 0))

    def title(self):
        if not self.game.skip:
            self.game.game = False
            self.title_index += 0.01
            text = self.fps_font.render(' ', False, 'white')
            self.title_scrn.fill('black')

            if 0 < int(self.title_index) < 1:
                pass

            if 2 < self.title_index < 3:
                text = self.fps_font.render('aboba games', False, 'white')

            if 3 < self.title_index < 4:
                text = self.fps_font.render('pon', False, 'white')

            if 5 < self.title_index < 6:
                text = self.fps_font.render('title', False, 'white')

            if 6 < self.title_index < 8:
                text = self.fps_font.render('another title', False, 'white')

            self.title_scrn.blit(text, (width / 2 - 100, height / 2 - 30))

            if self.title_index > 9:
                self.game.game = True

            else:
                pass

    def draw_crosshair(self, flag):
        if flag:
            mx, my = pygame.mouse.get_pos()
            self.cross.x = mx - 15
            self.cross.y = my - 15
            self.game.screen.blit(self.cross_im, self.cross)

    def draw_hotbar(self):
        hb_rect = pygame.rect.Rect(width // 2 - 150, height - 50, 250, 50)
        self.hotbar_scr.blit(hotbar, hb_rect)
        self.hotbar_scr.set_alpha(200)

        # working coords w: w // 2 - 148, h: h - 50
        for i in range(len(self.hb_things)):
            kolvo = 250 // len(self.hb_things)
            rect = (width // 2 - 148 + kolvo * i, height - 50)
            self.hotbar_scr.blit(pygame.transform.rotozoom(self.hb_things[i], 0, 0.5), rect)

            if self.game.tool.current_pic == self.hb_things[i]:
                pygame.draw.rect(self.hotbar_scr, 'white', (hb_rect[0] + kolvo * i, hb_rect[1], kolvo, 50), 2)

