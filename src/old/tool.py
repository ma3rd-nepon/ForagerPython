from player import *
from src.old import config


class Tool(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.anim_index = 0  # индекс анимации удара
        self.game = game
        self.current_pic = pickaxe_1
        self.pickaxe = pygame.transform.rotozoom(self.current_pic.convert_alpha(), 0, 1)  # основной пикча инструмента
        self.tool_hb = self.pickaxe.get_rect(center=pl_pos)
        self.current_tool = self.current_pic.convert_alpha()
        self.fx, self.fy = True, False  # поворот инструмента по х у
        self.angle = 0  # а что это?
        self.kirka = 0  # я непомню
        self.animation_speed = 0.48
        self.remove_en_perc = False

        self.pick_2 = False

        self.key = pygame.key.get_pressed()

        self.can_hit = True

    def moving(self):
        """Передвигает инструмент в руки игроку"""
        self.tool_hb.x = pl_pos[0]
        self.tool_hb.y = pl_pos[1] - 10

        if self.key[config.hit]:
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
            self.tool_hb.x = pl_pos[0] - 80

        else:
            if self.fx and not self.key[config.hit]:
                self.tool_hb.x = pl_pos[0] - 70

        self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def hit_new(self):
        """Новая анимация удара"""
        if self.can_hit:
            if not any([self.key[w], self.key[a], self.key[s], self.key[d]]):
                self.kirka += self.animation_speed
                if 0 <= self.kirka < 2:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70

                if int(self.kirka) == 2:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 45)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)
                    self.tool_hb.x = pl_pos[0] - 50
                    self.tool_hb.y = pl_pos[1] - 20

                if int(self.kirka) == 3:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 135)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0]
                    else:
                        self.tool_hb.x = pl_pos[0] - 100
                    self.tool_hb.y = pl_pos[1] - 10

                if int(self.kirka) == 4:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 90)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 20
                    else:
                        self.tool_hb.x = pl_pos[0] - 50
                    self.tool_hb.y = pl_pos[1] - 10

                if int(self.kirka) == 5:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 30)
                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 60
                    else:
                        self.tool_hb.x = pl_pos[0] - 40
                    self.tool_hb.y = pl_pos[1] - 30

                if int(self.kirka) == 6:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70

                if 5 < self.kirka < 12 and self.fx:
                    self.tool_hb.x = pl_pos[0] - 70

                if self.kirka > 11 or int(self.kirka) == 11:
                    self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                    self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

                    self.remove_en_perc = True

                    if self.fx:
                        self.tool_hb.x = pl_pos[0] - 70
                    self.kirka = 0