from tool import *
from ui import *
from entity import *
from player import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("marshmallow")

        self.key = pygame.key.get_pressed()
        self.ec = 0
        self.lst = []

        self.mask = pygame.transform.rotozoom(mask, 0, 1)

        self.level = Level()
        self.tool = Tool(self)
        self.ui = Player_UI(self)

        self.add_entity_to_map(5, sheep, coords=(52, 54))
        # self.add_entity_to_map(1, ghost)
        # self.add_entity_to_map(1, slime)
        # self.add_entity_to_map(1, player)
        self.add_entity_to_map(4, demon, is_enemy=True, coords=(38, 47))

        self.plyr = Player(self, (self.level.check_player_coords()),
                           (self.level.visible_sprites,), self.level.barrier_sprites)
        self.level.player = self.plyr

        self.r = False

        if self.ec:
            print('added', self.ec, 'entity to map')
            self.ec = 0

        for i in pickaxe:
            if pickaxe.index(i) > 4:
                break
            self.ui.hb_things.append(i)

    def draw(self):
        self.screen.fill('#337bc8')
        files = [self.level, self.tool]
        for i in files:  # оптимизация кода ееее
            i.draw()

    def update(self):
        ae = [self.ui, self.level, self.tool]
        for i in ae:
            i.update()

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

                if event.key == config.hide_hud:
                    self.ui.show_hud = not self.ui.show_hud

                if event.key == pygame.K_MINUS:
                    self.ui.health -= 10
                if event.key == 61:  # +
                    self.ui.health += 10

                if event.key in config.hotbar and config.hotbar.index(event.key) + 1 <= len(pickaxe):
                    self.tool.current_pic = pickaxe[config.hotbar.index(event.key)]

    def run(self):
        """Главный цикл"""
        while not not not not not self.r:
            arr = [self.draw, self.update, self.events]
            for i in arr:
                i()

    def add_entity_to_map(self, count: int, entity_anims: list, coords=('random', 'random'), is_enemy=False):
        """Добавить врага на карту"""
        for i in range(count):
            entt = Entity(self, self.level.barrier_sprites, is_enemy, entity_anims, coords)
            self.lst.append(entt.uid)
            self.level.visible_sprites.add(entt)
        self.ec += count


game = Game()
