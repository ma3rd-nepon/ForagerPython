import pygame.transform
import sys

from tool import *
from ui import *
from entity import *
from player import *
from day_night_time import *
from config import Configuration
from settings_menu import Settings
from settings import chanel0
from finish_window import FinishWind


class Game:
    def __init__(self, player_health, resources_num, monsters_num, boss_hp):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.deltatime = 0.025
        pygame.display.set_caption("marshmallow")

        self.resources_num = resources_num
        self.player_health = player_health
        self.monsters_num = monsters_num
        self.first_boss_hp = boss_hp

        self.key = pygame.key.get_pressed()
        self.ec = 0
        self.lst = []

        self.boss_hp = boss_hp
        self.mask = pygame.transform.rotozoom(mask, 0, 1)

        self.config = Configuration()
        self.level = Level()
        self.plyr = Player(self, (self.level.check_player_coords()), (self.level.visible_sprites,),
                           self.level.barrier_sprites)
        self.level.player = self.plyr
        self.boss = Boss(self, (self.plyr.player_on_map()), boss, limit=boss_hp)
        self.tool = Tool(self)
        self.ui = Player_UI(self, player_health, resources_num)
        self.sky = Sky()

        self.time_d = 0
        self.ubiraem = False
        self.total_exit = True

        self.add_entity_to_map(5, sheep, coords=(40, 10))
        self.add_entity_to_map(5, sheep, coords=(13, 27))
        self.add_entity_to_map(5, sheep, coords=(13, 40))
        self.add_entity_to_map(7, ghost, coords=(40, 38))
        # self.add_entity_to_map(7, slime, is_enemy=False, coords=(29, 23))
        self.add_entity_to_map(monsters_num, demon, is_enemy=True, coords=(13, 10))
        self.add_entity_to_map(monsters_num, demon, is_enemy=True, coords=(27, 38))
        self.add_entity_to_map(monsters_num, demon, is_enemy=True, coords=(35, 20))
        self.add_entity_to_map(monsters_num, demon, is_enemy=True, coords=(13, 38))

        self.level.visible_sprites.add(self.boss)

        vzyat = f'{pygame.key.name(self.config.hit).upper()} Взять'
        for _ in range(35):
            self.add_object(1, (random.randint(0, 80), random.randint(10, 70)), wood, vzyat)
            self.add_object(1, (random.randint(0, 80), random.randint(10, 70)), iron_piece, vzyat)
            self.add_object(1, (random.randint(0, 80), random.randint(10, 70)), gold_ingot, vzyat)

        self.r = False
        self.check = True

        self.background_music = pygame.mixer.Sound('../sound/game/day.wav')
        self.background_music.set_volume(self.config.game_mus_val)
        self.config.update_values()

    def draw(self):
        self.screen.fill('#69c3d1')  # 337bc8
        files = [self.level, self.tool]
        for i in files:  # оптимизация кода ееее
            i.draw()

    def update(self):
        ae = [self.ui, self.level, self.tool]
        for i in ae:
            i.update()

        if self.ui.health <= 0:  # персонаж умер
            self.add_amounts()
            total, wins = self.get_amounts()
            resources = sum((self.ui.loot[0][0][1], self.ui.loot[0][1][1], self.ui.loot[0][2][1]))
            finish = FinishWind(self.screen, 'sorry bro',
                                '../sprites/menu/cat1.jpg', '../sound/game/ggvp.mp3',
                                total, self.ui.days, resources, wins)
            chanel0.stop()
            finish.run()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                n = Game(self.player_health, self.resources_num, self.monsters_num, self.first_boss_hp)
                n.run()
                self.ui.attempt_num += 1
                self.ui.loot = [[[none, 0], [none, 0], [none, 0], [none, 0], [none, 0]],
                                [[none, 0], [none, 0], [none, 0], [none, 0], [none, 0]]]  # пакет с пакетами
            elif key[pygame.K_ESCAPE]:
                chanel3.unpause()
                self.r = True
                self.total_exit = False

        if (self.boss.health <= 0 and self.ui.loot[0][0][1] >= self.resources_num
                and self.ui.loot[0][1][1] >= self.resources_num
                and self.ui.loot[0][2][1] >= self.resources_num):  # все задания выполнены
            self.add_amounts(win=True)
            total, wins = self.get_amounts()
            resources = sum((self.ui.loot[0][0][1], self.ui.loot[0][1][1], self.ui.loot[0][2][1]))
            finish = FinishWind(self.screen, 'good job',
                                '../sprites/menu/ourbro.png', '../sound/game/win.mp3',
                                total, self.ui.days, resources, wins)
            chanel0.stop()
            finish.run()
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                n = Game(self.player_health, self.resources_num, self.monsters_num, self.first_boss_hp)
                n.run()
            elif key[pygame.K_ESCAPE]:
                chanel3.unpause()
                self.r = True
                self.total_exit = False

        if not self.sky.back:
            self.sky.display(self.deltatime)
        else:
            self.sky.display_back(self.deltatime)

        self.config.update_values()
        self.background_music.set_volume(self.config.game_mus_val)

        self.boss.health = self.boss_hp

        self.clock.tick(fps)
        self.level.current_fps = self.clock.get_fps()

        if self.ui.days == 2 and self.check:
            self.boss.letsgo = True
            self.ui.boss_bar = True
            self.check = False

        # pygame.display.flip()
        pygame.display.update()

    def events(self):
        """События игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.r = True
            if event.type == pygame.KEYDOWN:
                if event.key == self.config.pause:
                    pygame.mouse.set_visible(True)
                    chanel0.pause()
                    sett = Settings()
                    sett.run()

                if event.key == self.config.hit and self.tool.stop_key(*self.config.move):
                    self.tool.hitting = True
                    if self.plyr.rect.colliderect(self.boss.rect):
                        self.boss_hp -= 5

                if event.key == self.config.hide_hud and not self.ui.show[1]:
                    self.ui.show[0] = not self.ui.show[0]

                if event.key == self.config.inventory and self.ui.show[0]:
                    self.ui.show[1] = not self.ui.show[1]
                    self.tool.can_hit = not self.tool.can_hit
                    self.plyr.can_animate = not self.plyr.can_animate

                if event.key in self.config.hotbar and self.config.hotbar.index(event.key) + 1 <= len(
                        self.ui.hb_things):
                    if self.ui.hb_things:
                        self.tool.current_pic = self.ui.hb_things[self.config.hotbar.index(event.key)]

    def run(self):
        """Главный цикл"""
        chanel0.play(self.background_music, loops=-1)
        while not self.r:
            arr = [self.draw, self.update, self.events]
            for i in arr:
                i()
        if self.total_exit:
            pygame.quit()
            sys.exit()
        else:
            pass

    def add_entity_to_map(self, count: int, entity_anims: list, coords=('random', 'random'), is_enemy=False):
        """Добавить врага на карту"""
        for i in range(count):
            entt = Entity(self, self.level.barrier_sprites, is_enemy, entity_anims, coords)
            self.lst.append(entt.uid)
            self.level.visible_sprites.add(entt)

        self.ec += count

    def add_object(self, count: int, pos: tuple, sprite, text):
        for _ in range(count):
            obj = Object(self, text, self.add_to_inv, sprite, True, pos)
            self.level.visible_sprites.add(obj)

    def add_to_inv(self, img):
        for i in self.ui.loot:
            for j in i:
                if img == j[0]:
                    self.ui.loot[self.ui.loot.index(i)][i.index(j)][1] += 1
                    return
        else:
            for i in self.ui.loot:
                for j in i:
                    if j[0] is None:
                        self.ui.loot[self.ui.loot.index(i)][i.index(j)] = [img, 1]
                        return

    def add_amounts(self, win=False):
        with open('../src/special_txt_files/amounts.txt') as file:
            total_count, wins_count = map(int, file.readline().rstrip().split())
        print(total_count, wins_count)
        with open('../src/special_txt_files/amounts.txt', 'w') as file:
            file.write(f'{total_count + 1} {wins_count + 1}' if win else f'{total_count + 1} {wins_count}')

    def get_amounts(self):
        with open('../src/special_txt_files/amounts.txt') as file:
            return file.readline().rstrip().split()
