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


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.deltatime = 0.025
        pygame.display.set_caption("marshmallow")

        self.key = pygame.key.get_pressed()
        self.ec = 0
        self.lst = []

        self.boss_hp = 150

        self.mask = pygame.transform.rotozoom(mask, 0, 1)

        self.config = Configuration()

        self.level = Level()
        self.plyr = Player(self, (self.level.check_player_coords()), (self.level.visible_sprites,),
                           self.level.barrier_sprites)
        self.level.player = self.plyr
        self.boss = Boss(self, (self.plyr.player_on_map()), boss)
        self.tool = Tool(self)
        self.ui = Player_UI(self)
        self.sky = Sky()

        self.time_d = 0
        self.ubiraem = False

        self.add_entity_to_map(8, sheep, coords=(27, 64))
        self.add_entity_to_map(5, ghost, is_enemy=False, coords=(85, 77))
        self.add_entity_to_map(7, slime, is_enemy=False, coords=(82, 23))
        self.add_entity_to_map(4, demon, is_enemy=True, coords=(29, 15))
        self.level.visible_sprites.add(self.boss)

        vzyat = f'{pygame.key.name(self.config.hit).upper()} Взять'
        for _ in range(5):
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), wood, vzyat)
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), iron_piece, vzyat)
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), gold_ingot, vzyat)

        self.r = False
        self.check = True

        self.background_music = pygame.mixer.Sound('../sound/game/day.wav')
        self.background_music.set_volume(self.config.game_mus_val)
        self.config.update_values()

    # def rndm_pos(self):
    #     """Потом доделаю"""
    #     mp = self.level.load_layer('map.csv')
    #     x, y = random.randint(0, 100), random.randint(0, 100)
    #     if mp[x][y] == '-1':
    #         return x, y
    #     self.rndm_pos()

    def draw(self):
        self.screen.fill('#69c3d1')  # 337bc8
        files = [self.level, self.tool]
        for i in files:  # оптимизация кода ееее
            i.draw()

    def update(self):
        ae = [self.ui, self.level, self.tool]
        for i in ae:
            i.update()

        if not self.sky.back:
            self.sky.display(self.deltatime)
        else:
            self.sky.display_back(self.deltatime)

        self.config.update_values()
        self.background_music.set_volume(self.config.game_mus_val)

        self.boss.health = self.boss_hp

        self.clock.tick(fps)
        self.level.current_fps = self.clock.get_fps()

        if self.boss.health <= 0 and all([[iron_piece, 7] in loot, [wood, 4] in loot]):
            # экран победы
            print('ura')

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
                    self.sky.pause = True
                    chanel0.pause()
                    sett = Settings()
                    sett.run()

                    # нужно сделать чтобы курсор появился
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

                if event.key in self.config.hotbar and self.config.hotbar.index(event.key) + 1 <= len(self.ui.hb_things):
                    if self.ui.hb_things:
                        self.tool.current_pic = self.ui.hb_things[self.config.hotbar.index(event.key)]

    def run(self):
        """Главный цикл"""
        chanel0.play(self.background_music, loops=-1)
        while not self.r:
            arr = [self.draw, self.update, self.events]
            for i in arr:
                i()
        pygame.quit()
        sys.exit()

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
        for i in loot:
            for j in i:
                if img == j[0]:
                    loot[loot.index(i)][i.index(j)][1] += 1
                    return
        else:
            for i in loot:
                for j in i:
                    if j[0] is None:
                        loot[loot.index(i)][i.index(j)] = [img, 1]
                        return


game = Game()
