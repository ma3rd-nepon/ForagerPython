import pygame.transform
import sys

from tool import *
from ui import *
from entity import *
from player import *
from day_night_time import *
from config import game_mus_val


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

        self.mask = pygame.transform.rotozoom(mask, 0, 1)

        self.level = Level()
        self.plyr = Player(self, (self.level.check_player_coords()),
                           (self.level.visible_sprites,), self.level.barrier_sprites)
        self.level.player = self.plyr
        self.tool = Tool(self)
        self.ui = Player_UI(self)
        self.sky = Sky()

        self.time_d = 0
        self.ubiraem = False

        self.add_entity_to_map(8, sheep, coords=(27, 64))
        self.add_entity_to_map(5, ghost, is_enemy=False, coords=(85, 77))
        self.add_entity_to_map(7, slime, is_enemy=False, coords=(82, 23))
        # self.add_entity_to_map(1, player)
        self.add_entity_to_map(4, demon, is_enemy=True, coords=(29, 15))

        vzyat = f'{pygame.key.name(config.hit).upper()} Взять'
        for _ in range(5):
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), wood, vzyat)
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), iron_piece, vzyat)
            self.add_object(1, (random.randint(0, 100), random.randint(0, 100)), gold_ingot, vzyat)

        self.r = False

        self.background_music = pygame.mixer.Sound('../sound/game/day.wav')
        self.background_music.set_volume(game_mus_val)

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

        self.clock.tick(fps)
        self.level.current_fps = self.clock.get_fps()

        pygame.display.flip()
        # pygame.display.update()

    def events(self):
        """События игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.r = True
            if event.type == pygame.KEYDOWN:
                if event.key == config.hit and self.tool.stop_key(*config.move):
                    self.tool.hitting = True

                if event.key == config.hide_hud and not self.ui.show[1]:
                    self.ui.show[0] = not self.ui.show[0]
                if event.key == config.inventory and self.ui.show[0]:
                    self.ui.show[1] = not self.ui.show[1]
                    self.tool.can_hit = not self.tool.can_hit
                    self.plyr.can_animate = not self.plyr.can_animate

                if event.key == pygame.K_MINUS:
                    for i in loot:
                        for item in i:
                            if item[0] is not None:
                                loot[loot.index(i)][i.index(item)] = (none, 1)
                                return

                if event.key == 61:  # +
                    for i in loot:
                        for item in i:
                            if item[0] is None:
                                loot[loot.index(i)][i.index(item)] = (random.choice([wood, charcoal, iron_piece, gold_ingot, mask]), random.randint(1, 100))
                                return

                if event.key in config.hotbar and config.hotbar.index(event.key) + 1 <= len(self.ui.hb_things):
                    if self.ui.hb_things:
                        self.tool.current_pic = self.ui.hb_things[config.hotbar.index(event.key)]

    def run(self):
        """Главный цикл"""
        pygame.mixer.Channel(0).play(self.background_music)
        while not not not not not self.r:
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
