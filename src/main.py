import pygame

from map import *
from player import *
from settings import *
from imgs import *
from src import config
from tool import *
from ui import *
from console import convert


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)

        self.map, self.player, self.tool, self.ui = [None for _ in range(4)]

        pygame.display.set_caption("alone marshmallow")

        self.key = pygame.key.get_pressed()

        self.game = True # если она фолс то игра не будет работать (запустится сама после загрузочного экрана)
        self.skip = True  # если тру то пропустит начальный екран\

        if not self.game:
            self.skip = False

        self.clock = pygame.time.Clock()
        self.delta_time = 1

        pygame.mouse.set_visible(False)
        self.last = pygame.time.get_ticks()

        self.spawn = False  # флаг для создания блоков в рандом месте

        self.pause = False  # если тру то игра на паузе

        self.console = False
        self.com = []

        # self.instruct()  # пишет в консоль клавиши

        self.start_game()

    def start_game(self):
        """Определение всех классов"""
        self.map = Map(self)
        self.player = Player(self)
        self.tool = Tool(self)
        self.ui = Player_UI(self)

        self.ui.title()
        for i in picks:
            self.ui.hb_things.append(i)

    def update(self):
        """Обновление всех штук изображаемых на экране"""
        if self.game:
            if not self.pause:
                self.tool.update()

            self.player.update()
            self.ui.pause()
        # pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

            if self.tool.remove_en_perc:
                self.ui.percentage -= 1
                self.tool.remove_en_perc = False

            self.key = pygame.key.get_pressed()

            if self.ui.percentage == 0:
                self.tool.can_hit = False
            else:
                self.tool.can_hit = True

        self.ui.update()

        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)

    def draw(self):
        """Отрисовка всех штук на экране"""
        if not self.pause and self.game:
            self.screen.fill('#337bc8')
            self.map.draw()

            if self.player.tx:
                self.player.draw_particles(pl_pos[0] + 40, pl_pos[1] + 70)
            else:
                self.player.draw_particles(pl_pos[0] - 20, pl_pos[1] + 70)

            self.player.draw()
            self.tool.draw()

            if any([not -5 < self.player.hitbox_rect[0] < width, not -5 < self.player.hitbox_rect[1] < height]):
                print('плеер ходит там где ненадо')
        else:
            if self.console:
                pygame.draw.rect(self.screen, 'white', (0, 40, 40, 40))

    def events(self):
        """Обработка событий игры"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if not self.pause:
                    if e.key == config.dash:
                        if not self.pause:
                            self.player.dash()

                    if e.key == config.hide_hud:
                        self.ui.show_hud = not self.ui.show_hud

                    if e.key == config.skip_title:
                        self.ui.title_index = 11

                    if e.key == config.spawn_blocks:
                        self.spawn = not self.spawn
                        self.map.rechoice()
                        if self.spawn:
                            print('random blocks spawned!')
                        else:
                            print('random blocks removed!')

                    if e.key in config.hotbar and config.hotbar.index(e.key) + 1 <= len(picks):
                        self.tool.current_pic = picks[config.hotbar.index(e.key)]

                if e.key == config.console and self.pause:
                    self.console = True

                if e.key == config.pause:
                    if self.game:
                        self.pause = not self.pause

    def run(self):
        """Запуск игры и её главный цикл"""
        while True:
            self.command()
            self.events()
            self.update()
            if self.game:
                self.draw()
                if self.spawn:
                    self.map.spawn_blocks()
            else:
                self.ui.title()

    def instruct(self):
        """Вывод всех используемых клавиш и их назначение"""
        print('''
help - this list
money (int) - set money count
time (int) (int) - set time
crash game - crash game (bruh)
energy (int) - set energy
spr (int) - set tool sprite
''')

    def command(self):
        if self.pause:
            if self.console:
                if self.key[13]:
                    command = convert(self.com)
                    print('command: ' + command)
                    if command == 'help':
                        self.instruct()

                    if 'money' in command:
                        command = command.replace('money ', '')
                        try:
                            self.ui.coin_count = int(command)
                        except ValueError:
                            print('wrong written command')

                    if command == 'crash game':
                        raise WindowsError('idk what happened')

                    if 'energy' in command:
                        command = command.replace('energy ', '')
                        try:
                            self.ui.percentage = int(command)
                        except ValueError:
                            print('wrong written command')

                    if 'time' in command:
                        command = command.replace('time ', '')
                        command = command.split(' ')
                        try:
                            self.ui.time = [int(command[0]), int(command[1])]
                        except ValueError:
                            print('wrong time')

                    if 'spr' in command:
                        command = command.replace('spr ', '')
                        try:
                            self.tool.current_pic = picks[int(command) - 1]
                        except IndexError:
                            print('error')
                    else:
                        pass
                    self.console = False
                    self.com.clear()
                for i in pygame.event.get():
                    if i.type == 768:
                        self.com.append(i.key)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
