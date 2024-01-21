import pygame
from settings import resolution

pygame.init()


class Sky:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.display_surf = pygame.display.get_surface()
        self.surface = pygame.Surface(resolution)
        self.back = False
        self.start_color, self.end_color = [255, 255, 255], (38, 101, 189)

    def display(self, dt):
        seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        if seconds > 30:
            for i, value in enumerate(self.end_color):
                if self.start_color[i] > value:
                    self.start_color[i] -= 3 * dt

            self.surface.fill(self.start_color)
            self.display_surf.blit(self.surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            if len([1 for i, v in enumerate(self.start_color) if v <= self.end_color[i]]) == 3:
                seconds = (pygame.time.get_ticks() - self.start_time) / 1000
                if seconds > 80:
                    self.back = True
                    self.start_color, self.end_color = [38, 101, 189], (255, 255, 255)
                    self.start_time = pygame.time.get_ticks()

    def display_back(self, dt):
        for i, value in enumerate(self.end_color):
            if self.start_color[i] < value:
                self.start_color[i] += 3 * dt

        self.surface.fill(self.start_color)
        self.display_surf.blit(self.surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        if len([1 for i, v in enumerate(self.start_color) if v >= self.end_color[i]]) == 3:
            seconds = (pygame.time.get_ticks() - self.start_time) / 1000
            if seconds > 65:
                self.back = False
                self.start_color, self.end_color = [255, 255, 255], (38, 101, 189)
                self.start_time = pygame.time.get_ticks()
