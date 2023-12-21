from settings import *
from imgs import *
import config

pl_pos = (width // 2, height // 2)
w, a, s, d = config.up, config.left, config.down, config.right


class Tool(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.anim_index = 0
        self.game = game
        self.current_pic = pickaxe[0]
        self.pickaxe = pygame.transform.rotozoom(self.current_pic.convert_alpha(), 0, 1)
        self.tool_hb = self.pickaxe.get_rect(center=pl_pos)
        self.current_tool = self.current_pic.convert_alpha()
        self.fx, self.fy = True, False
        self.angle = 0
        self.kirka = 0
        self.animation_speed = 0.48
        self.remove_en_perc = False

        self.pick_2 = False

        self.key = pygame.key.get_pressed()

        self.can_hit = True

    def stop_key(self, *args):
        if any([pygame.key.get_pressed()[arg] for arg in args]):
            return False
        return True

    def moving(self):
        """Передвигает инструмент в руки игроку"""
        # self.tool_hb.x = pl_pos[0]
        self.tool_hb.y = pl_pos[1] - 30

        if self.key[config.hit] and self.stop_key(w, a, s, d):
            self.hit_new()
        else:
            self.current_tool = self.current_pic
            self.kirka = 0
            self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def update(self):
        """Обновление отрисовки инструмента"""
        self.moving()
        self.flipping()

        self.key = pygame.key.get_pressed()

    def draw(self):
        """Рисование инструмента"""
        self.game.screen.blit(self.pickaxe, self.tool_hb)

    def flipping(self):
        """Поворот инструмента в зависимости от поворота игрока"""
        if self.key[config.left] and not self.key[config.right]:
            self.fx = False
            self.tool_hb.x = pl_pos[0] + 10
        elif self.key[config.right] and not self.key[config.left]:
            self.fx = True
            self.tool_hb.x = pl_pos[0] - 100

        else:
            if self.fx and self.stop_key(config.hit):
                self.tool_hb.x = pl_pos[0] - 90

        self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def hit_new(self):
        """Новая анимация удара"""
        if self.can_hit:
            if self.stop_key(w, a, s, d):
                self.kirka += self.animation_speed
                if 0 <= self.kirka < 4:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    else:
                        self.tool_hb.x = pl_pos[0] - 20
                    self.tool_hb.y = pl_pos[1] - 30

                if int(self.kirka) == 4:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 45)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 50
                    else:
                        self.tool_hb.x = pl_pos[0] - 75
                    self.tool_hb.y = pl_pos[1] - 50

                if int(self.kirka) == 5:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 135)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0]
                    else:
                        self.tool_hb.x = pl_pos[0] - 120
                    self.tool_hb.y = pl_pos[1] - 30

                if int(self.kirka) == 6:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 90)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 20
                    else:
                        self.tool_hb.x = pl_pos[0] - 50
                    self.tool_hb.y = pl_pos[1] - 30

                if int(self.kirka) == 7:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 30)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 60
                    else:
                        self.tool_hb.x = pl_pos[0] - 40
                    self.tool_hb.y = pl_pos[1] - 50

                if int(self.kirka) == 8:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    else:
                        self.tool_hb.x = pl_pos[0] - 20

                if 8 < self.kirka < 15 and self.fx:
                    self.tool_hb.x = pl_pos[0] - 70

                if self.kirka > 9 or int(self.kirka) == 9:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    self.game.ui.percentage -= 1

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    self.kirka = 0

    def break_block(self):
        """Не сделал пока что"""
        pom = self.game.plyr.player_on_map()
        wmp = self.game.level.load_layer('map.csv')

        if self.fx:
            # ломаем справа
            print(wmp[pom[0]][pom[1]], pom)
        else:
            # ломаем слева
            print(wmp[pom[0]][pom[1]], pom)
