import pygame

from settings import *
from imgs import *
from player import *


class Tool(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.anim_index = 0
        self.game = game
        self.pickaxe = pygame.transform.rotozoom(pickaxe_1.convert_alpha(), 0, 1)
        self.tool_hb = self.pickaxe.get_rect(center=pl_pos)
        self.current_tool = pickaxe_1.convert_alpha()
        self.fx, self.fy = True, False
        self.angle = 0

    def moving(self):
        self.tool_hb.x = pon[0]
        self.tool_hb.y = pon[1] - 10

        key = pygame.key.get_pressed()
        if key[pygame.K_n]:
            self.hit()
        else:
            self.current_tool = pickaxe_1
            self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def update(self):
        self.moving()
        self.flipping()

    def draw(self):
        self.game.screen.blit(self.pickaxe, self.tool_hb)

    def flipping(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.fx = False
            self.tool_hb.x = pon[0] + 10
        elif key[pygame.K_d]:
            self.fx = True
            self.tool_hb.x = pon[0] - 80

        else:
            if self.fx:
                self.tool_hb.x = pon[0] - 70

        self.pickaxe = pygame.transform.flip(self.current_tool, self.fx, self.fy)

    def hit(self):
        self.anim_index += 0.1

        if self.anim_index >= len(im_h):
            self.anim_index = 0

        if not self.fx:
            self.tool_hb.x = pon[0] - 50
        self.current_tool = pygame.transform.rotozoom(im_h[int(self.anim_index)], 0, 1)
        fx = not self.fx
        self.pickaxe = pygame.transform.flip(self.current_tool, fx, self.fy)
