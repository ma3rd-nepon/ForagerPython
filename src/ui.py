from settings import *
from imgs import *

bgcolor = 'black'
textcolor = 'white'


class Player_UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.font.init()
        self.game = game

        self.pause_ui = pygame.Surface((width, height), pygame.SRCALPHA)

        self.hotbar_scr = pygame.Surface((width, height), pygame.SRCALPHA)

        self.coin_image = pygame.transform.rotozoom(coin.convert_alpha(), 0, 0.5)
        self.coin_hb = self.coin_image.get_rect()
        self.coin_hb.x, self.coin_hb.y = 20, height - 70

        self.health = 100
        self.heart_image = pygame.transform.rotozoom(heart.convert_alpha(), 0, 0.35)
        self.heart_hb = self.heart_image.get_rect()
        self.heart_hb.move_ip(10, 10)

        self.coin_count = 0  # колво монет
        self.coin_font = pygame.font.Font(font, 40)  # шрифт для цифры
        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, textcolor)  # рендер текста

        self.fps_font = pygame.font.Font(font, 20)
        self.fps = self.fps_font.render(f"{self.game.clock.get_fps()}", False, textcolor)

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

    def draw(self):
        """Отрисовка всех элементов интерфейса"""
        self.game.screen.blit(self.heart_image, self.heart_hb)

        self.game.screen.blit(self.coin_image, self.coin_hb)
        self.game.screen.blit(self.coin_count_text, (90, height - 55))

        self.game.screen.blit(self.fps, (width - 35, 10))

        self.game.screen.blit(self.hotbar_scr, (0, 0))

        self.draw_health(self.health)

        self.draw_energy(self.percentage)

        self.draw_timer()

        self.draw_crosshair(True)

        self.draw_hotbar()

    def update(self):
        """Обновление интерфейса"""
        pygame.mouse.set_visible(not self.show_hud)

        if self.coin_count > 10000:
            self.coin_count = 10000

        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, textcolor, bgcolor)
        self.fps = self.fps_font.render(f"{int(self.game.clock.get_fps())}", False, textcolor, bgcolor)

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

    def draw_health(self, health):
        perc = float(health / 100)
        if perc < 0:
            perc = 0
        pygame.draw.rect(self.game.screen, 'black', (50, 15, 105, 30))
        pygame.draw.rect(self.game.screen, 'red', (55, 20, 95 * perc, 20))

    def draw_energy(self, percent: int):
        """Отрисовка полоски энергии"""
        perc = float(percent / 100)
        if perc < 0:
            perc = 0
        pygame.draw.rect(self.game.screen, 'black', (10, 60, 105, 30))
        pygame.draw.rect(self.game.screen, '#90EE90', (15, 65, 95 * perc, 20))

    def draw_timer(self):
        """Отображает игровое время"""
        timee = self.fps_font.render(f"{self.time[0]}:{str(self.time[1])}", False, textcolor, bgcolor)
        self.game.screen.blit(timee, (width - 80, 40))

    def draw_crosshair(self, flag):
        if flag:
            self.cross.center = pygame.mouse.get_pos()
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

