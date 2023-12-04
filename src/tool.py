import pygame

from settings import *
from imgs import *
from player import *


class Tool(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.anim_index = 0  # индекс анимации удара
        self.game = game
        self.current_pic = pickaxe_3
        self.pickaxe = pygame.transform.rotozoom(self.current_pic.convert_alpha(), 0, 1)  # основной пикча инструмента
        self.tool_hb = self.pickaxe.get_rect(center=pl_pos)
        self.current_tool = self.current_pic.convert_alpha()
        self.fx, self.fy = True, False  # поворот инструмента по х у
        self.angle = 0  # а что это?
        self.kirka = 0  # я непомню
        self.animation_speed = 0.3  # скорость анимации
        self.remove_en_perc = False  # если тру то отнимет 1 процент от энергии, потом поумному закостылю

        self.pick_2 = False

    def moving(self):
        """Передвигает инструмент в руки игроку"""
        self.tool_hb.x = pon[0]
        self.tool_hb.y = pon[1] - 10

        key = pygame.key.get_pressed()
        if key[pygame.K_n]:
            self.hit()
        else:
            self.current_tool = self.current_pic
            self.kirka = 0
            self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def update(self):
        """Обновление отрисовки инструмента"""
        self.moving()
        self.flipping()

    def draw(self):
        """Рисование инструмента"""
        self.game.screen.blit(self.pickaxe, self.tool_hb)

    def flipping(self):
        """Поворот инструмента в зависимости от поворота игрока"""
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and not key[pygame.K_d]:
            self.fx = False
            self.tool_hb.x = pon[0] + 10
        elif key[pygame.K_d] and not key[pygame.K_a]:
            self.fx = True
            self.tool_hb.x = pon[0] - 80

        else:
            if self.fx and not key[pygame.K_n]:
                self.tool_hb.x = pon[0] - 70

        self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def hit(self):
        """Анимация удара киркой"""
        key = pygame.key.get_pressed()
        if not any([key[pygame.K_w], key[pygame.K_a], key[pygame.K_s], key[pygame.K_d]]):
            self.kirka += self.animation_speed
            if self.kirka == 0:
                self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)
            if int(self.kirka) == 1:
                self.current_tool = pygame.transform.rotate(self.current_pic, -45)
                self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10

            if int(self.kirka) == 2:
                self.current_tool = pygame.transform.rotate(self.current_pic, -30)
                self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10

            if int(self.kirka) == 3:
                self.current_tool = pygame.transform.rotate(self.current_pic, 0)
                self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10

            if int(self.kirka) == 4:
                self.current_tool = pygame.transform.rotate(self.current_pic, 50)
                self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 30

            if int(self.kirka) == 5:
                self.current_tool = pygame.transform.rotate(self.current_pic, 90)
                if self.fx:
                    self.tool_hb.x = pon[0] - 20
                else:
                    self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10

            if int(self.kirka) > 5:
                self.animation_speed = -self.animation_speed
                self.remove_en_perc = True
                if self.fx:
                    self.tool_hb.x = pon[0] - 20
                else:
                    self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10
            if int(self.kirka) <= 0:
                self.animation_speed = abs(self.animation_speed)
                self.tool_hb.x = pon[0] - 50
                self.tool_hb.y = pon[1] - 10

