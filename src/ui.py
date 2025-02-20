from imgs import *
from config import Configuration

bgcolor = 'black'
textcolor = 'white'
none = None


class Player_UI:
    def __init__(self, game, player_health, resources_num):
        pygame.font.init()
        self.game = game

        self.pause_ui = pygame.Surface((width, height), pygame.SRCALPHA)
        self.hotbar_scr = pygame.Surface((width, height), pygame.SRCALPHA)

        self.coin_image = pygame.transform.rotozoom(coin.convert_alpha(), 0, 0.5)
        self.coin_hb = self.coin_image.get_rect()
        self.coin_hb.x, self.coin_hb.y = 20, height - 70

        self.loot = [[[none, 0], [none, 0], [none, 0], [none, 0], [none, 0]],
                     [[none, 0], [none, 0], [none, 0], [none, 0], [none, 0]]]  # пакет с пакетами
        self.resources_num = resources_num

        self.health = player_health
        self.defoult_health = player_health
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
        self.days = 1
        self.time = [12, 0]
        self.imdxxx = 0

        self.hb_things = []
        self.key = pygame.key.get_pressed()
        self.show = [False, False]  # 1 - show hud, 2 - show inventory

        self.inv = pygame.Surface((width, height), pygame.SRCALPHA)
        self.animate_player = 0
        self.attempt_num = 1
        self.config = Configuration()
        self.boss_bar = False

    def draw(self):
        """Отрисовка всех элементов интерфейса"""
        self.game.screen.blit(self.heart_image, self.heart_hb)

        self.game.screen.blit(self.coin_image, self.coin_hb)
        self.game.screen.blit(self.coin_count_text, (90, height - 55))

        self.game.screen.blit(self.fps, (width - 35, 10))

        self.game.screen.blit(self.hotbar_scr, (0, 0))

        if self.boss_bar and self.game.boss_hp > 0:
            self.draw_bar(self.game.boss_hp)

        self.draw_timer()

        self.draw_hotbar()

        self.draw_inventory(self.show[1])

        self.draw_health(self.health)

        self.draw_energy(self.percentage)

        self.draw_crosshair(True)

    def update(self):
        """Обновление интерфейса"""
        pygame.mouse.set_visible(not self.show[0])

        if self.coin_count > 10000:
            self.coin_count = 10000

        self.coin_count_text = self.coin_font.render(str(self.coin_count), False, textcolor, bgcolor)
        self.fps = self.fps_font.render(f"{int(self.game.clock.get_fps())}", False, textcolor, bgcolor)

        if self.show[0]:
            self.draw()

        self.imdxxx += 10  # скорость течения времени
        if int(self.imdxxx) == 60:
            self.imdxxx = 0
            self.time[1] += 1

        if self.time[1] == 60:
            self.time[1] = 0
            self.time[0] += 1
            self.imdxxx = 0
            if self.time[0] == 24:
                self.time[0] = 0
                self.days += 1

    def draw_bar(self, count):
        perc = float(count / 100)
        rect1 = (250, 20, 500 * 1.5, 50)
        rect2 = (255, 25, 490 * perc, 40)
        pygame.draw.rect(self.game.screen, 'black', rect1)
        pygame.draw.rect(self.game.screen, 'red', rect2)

    def draw_health(self, health):
        perc = float(health / 100)

        if self.show[1]:
            rect1 = (900, 30, 200, 50)
            rect2 = (905, 35, 190 * perc, 40)
        else:
            rect1 = (50, 15, self.defoult_health, 30)
            rect2 = (55, 20, 95 * perc, 20)
        pygame.draw.rect(self.game.screen, 'black', rect1)
        pygame.draw.rect(self.game.screen, 'red', rect2)

    def draw_energy(self, percent: int):
        """Отрисовка полоски энергии"""
        perc = float(percent / 100)
        if perc < 0:
            perc = 0

        if not self.show[1]:
            rect1 = (10, 60, 105, 30)
            rect2 = (15, 65, 95 * perc, 20)
        else:
            rect1 = (900, 80, 200, 50)
            rect2 = (905, 85, 190 * perc, 40)
        pygame.draw.rect(self.game.screen, 'black', rect1)
        pygame.draw.rect(self.game.screen, '#90EE90', rect2)

    def draw_timer(self):
        """Отображает игровое время"""
        days = self.fps_font.render(f"day {self.days}", False, textcolor, bgcolor)
        timee = self.fps_font.render(f"{self.time[0]}:{str(self.time[1])}", False, textcolor, bgcolor)
        self.game.screen.blit(timee, (width - 80, 40))
        self.game.screen.blit(days, (width - 80, 40))

    def draw_crosshair(self, flag):
        if flag:
            self.cross.center = pygame.mouse.get_pos()
            self.game.screen.blit(self.cross_im, self.cross)

    def draw_hotbar(self):
        if not self.show[1]:
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

    def draw_tasks(self):
        fontt = pygame.font.Font(None, 30)
        name = fontt.render("Текущие задачи:", False, 'white')
        task1 = fontt.render(f"Собрать {self.resources_num} железа, {self.resources_num} "
                             f"золота и {self.resources_num} дерева", False, 'white')
        task2 = fontt.render("Убить чертилу", False, 'white')
        arr = [name, task1, task2]
        self.game.screen.blit(arr[0], (100, 500))
        self.game.screen.blit(arr[1], (100, 540))
        self.game.screen.blit(arr[2], (100, 580))

    def draw_inventory(self, flag):
        if flag:
            self.animate_player += 0.15
            pygame.draw.rect(self.inv, (0, 0, 0, 120), (0, 0, width, height))

            wid = 5
            x = 1
            arr_rect = []
            arr_imgs = []
            mos = pygame.mouse.get_pos()

            for i in range(len(self.loot[0]) * 2):
                cw = 115 + (i * 90) + wid
                if i >= 5:
                    x = 2
                    cw = 115 + ((i - 5) * 90) + wid
                ch = (90 + wid) * x
                ssize = 80

                rect = pygame.Rect((cw, ch, ssize + wid, ssize + wid))
                arr_rect.append(rect)
                pygame.draw.rect(self.inv, (0, 0, 0), rect, wid)

            for stroka in self.loot:
                for i in stroka:
                    img = i[0]
                    arr_imgs.append(img)

                    if img is not None:
                        coff = stroka.index(i)
                        count = i[1]
                        text = self.fps_font.render(f"{count}", False, textcolor)

                        ch = (90 + wid) * (self.loot.index(stroka) + 1)  # cell height
                        cw = 115 + coff * 90 + wid  # cell width
                        ssize = 80  # item sprites size

                        self.inv.blit(img, (cw, ch, ssize, ssize))  # img not int type pycharm stupid
                        if img != none:
                            self.inv.blit(text, (cw + 10, ch + 10))

                if pygame.mouse.get_pressed()[0] and len(arr_imgs) == 10:
                    for rect in arr_rect:
                        if rect.collidepoint(mos):
                            da = arr_imgs[arr_rect.index(rect)]
                            # print(f"{arr_rect.index(rect) + 1} клетка")
            self.draw_tasks()

            if self.animate_player >= len(player[0]):
                self.animate_player = 0
            self.inv.blit(player[0][int(self.animate_player)], (950, 350))

            self.game.screen.blit(self.inv, (0, 0))
