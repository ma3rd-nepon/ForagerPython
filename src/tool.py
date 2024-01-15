from settings import *
from imgs import *
import config

pl_pos = (width // 2, height // 2)
w, a, s, d = config.up, config.left, config.down, config.right


class Tool(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.mixer.init()
        self.game = game
        self.current_pic = none
        self.pickaxe = pygame.transform.rotozoom(self.current_pic.convert_alpha(), 0, 1)
        self.tool_hb = self.pickaxe.get_rect()
        self.current_tool = self.current_pic.convert_alpha()
        self.fx, self.fy = not self.game.plyr.tx, self.game.plyr.ty

        self.hit_index = 0
        self.animation_speed = 0.48
        self.hitting = False
        self.hit_sound = pygame.mixer.Sound('../sound/player/hit.wav')
        self.hit_sound.set_volume(config.sound_ef_val)

        self.key = pygame.key.get_pressed()

        self.can_hit = True

    def stop_key(self, *args):
        if any([pygame.key.get_pressed()[arg] for arg in args]):
            return False
        return True

    def update(self):
        """Обновление отрисовки инструмента"""
        self.moving()
        self.flipping()
        if not self.game.ui.show[1]:
            if self.current_pic in pickaxe:
                self.hit_pickaxe()
                self.what()
            else:
                self.udar_rukoy()
        if self.game.ui.percentage > 0:
            self.can_hit = True
        else:
            self.can_hit = False

        self.key = pygame.key.get_pressed()
        self.fx, self.fy = not self.game.plyr.tx, self.game.plyr.ty

    def draw(self):
        """Рисование инструмента"""
        self.game.screen.blit(self.pickaxe, self.tool_hb)

    def moving(self):
        if not self.hitting:
            if self.fx:
                self.tool_hb.x = pl_pos[0] - 90
            else:
                self.tool_hb.x = pl_pos[0]

    def flipping(self):
        """Поворот инструмента в зависимости от поворота игрока"""
        if not self.game.ui.show[1]:
            if self.key[config.left] and not self.key[config.right]:
                self.tool_hb.x = pl_pos[0] + 10
            if self.key[config.right] and not self.key[config.left]:
                self.tool_hb.x = pl_pos[0] - 100

        self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def udar_rukoy(self):
        if self.hitting:
            self.hit_index += 0.5

            if self.hit_index >= len(hit_none):
                pygame.mixer.Channel(2).play(self.hit_sound)
                self.hit_index = 0
                self.hitting = False
                return

            self.current_pic = hit_none[int(self.hit_index)]
            self.pickaxe = pygame.transform.flip(self.current_pic, not self.fx, self.fy)

            self.tool_hb.y = (height // 2) - 10
            if not self.fx:
                kek = 70
            else:
                kek = 0
            self.tool_hb.x = (width // 2) - kek

    def hit_pickaxe(self):
        if self.hitting and self.can_hit:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('../sound/player/hit.wav'))
            if self.can_hit and self.stop_key(w, a, s, d):
                self.hit_index += self.animation_speed
                i = 2

                if 0 <= self.hit_index < i:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    else:
                        self.tool_hb.x = pl_pos[0] - 20
                    self.tool_hb.y = pl_pos[1] - 30

                if i < self.hit_index < i + 1:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 45)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 50
                    else:
                        self.tool_hb.x = pl_pos[0] - 75
                    self.tool_hb.y = pl_pos[1] - 50

                if i + 1 < self.hit_index < i + 2:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 135)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0]
                    else:
                        self.tool_hb.x = pl_pos[0] - 120
                    self.tool_hb.y = pl_pos[1] - 30

                if i + 2 < self.hit_index < i + 3:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 90)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 20
                    else:
                        self.tool_hb.x = pl_pos[0] - 70
                    self.tool_hb.y = pl_pos[1] - 30

                if i + 3 < self.hit_index < i + 4:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 30)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 80
                    else:
                        self.tool_hb.x = pl_pos[0] - 40
                    self.tool_hb.y = pl_pos[1] - 50

                if i + 4 < self.hit_index < i + 5:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    else:
                        self.tool_hb.x = pl_pos[0] - 20
                    self.tool_hb.y = pl_pos[1] - 30

                if i + 6 < self.hit_index < i + 12 and self.fx:
                    self.tool_hb.x = pl_pos[0] - 70
                    self.tool_hb.y = pl_pos[1] - 30

                if int(self.hit_index) >= i + 7:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    self.game.ui.percentage -= 1

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    self.hit_index = 0
                    self.hitting = False
        else:
            self.tool_hb.y = pl_pos[1] - 30

            self.current_tool = self.current_pic
            self.hit_index = 0
            self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def what(self):
        if not self.stop_key(w, a, s, d):
            self.hitting = False

    def break_block(self):
        """Не сделал пока что"""
        pom = self.game.plyr.player_on_map()
        wmp = self.game.level.load_layer('map.csv')

        if self.fx:
            print(wmp[pom[0]][pom[1]], pom)
        else:
            print(wmp[pom[0]][pom[1]], pom)
