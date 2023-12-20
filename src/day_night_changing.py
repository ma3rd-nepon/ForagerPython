import pygame

# from settings import w, h, resolution, fps
resolution = w, h = 500, 500
timer_event_type = 3600


# ой как же криво это работает((((((((
class DayNight:
    def __init__(self, surface):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.alpha = 0
        self.day_changing = True
        self.hours_24 = 0
        self.running = True
        self.delay = 3600
        self.type = 0
        # self.day_night_time_delay = 10000
        pygame.time.set_timer(timer_event_type, self.delay)

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def run(self):
        while self.running:
            # self.changing()
            # self.update()
            self.events()
        pygame.display.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.running = False
            # if event.type == timer_event_type:
            #     self.changing()
            self.changing()
            self.surface.fill((0, 0, 0))
            self.draw_rect_alpha(self.surface, (0, 0, 255, self.alpha), (0, 0, w, h))
            pygame.display.flip()

    def changing(self):
        self.clock.tick(1)
        self.hours_24 += 10
        print(f'{self.hours_24} врееемя')
        if self.hours_24 <= 120:
            self.alpha_change(0)
            # self.type = 0
        elif 120 < self.hours_24 <= 180:
            self.alpha_change(1)
            # self.type = 1
        elif 180 < self.hours_24 <= 300:
            self.alpha_change(2)
            # self.type = 2
        elif 300 < self.hours_24 < 360:
            self.alpha_change(3)
            # self.type = 3
        elif self.hours_24 == 360:
            self.hours_24 = 0
        else:
            print('Да такого быть не может')

    def alpha_change(self, n):
        if n == 0:  # утро
            self.alpha = 0
        elif n == 1:  # темнеет
            if self.alpha < 190:
                self.alpha += 10
        elif n == 2:  # ночь
            self.alpha = 200
        elif n == 3:  # светлеет
            if self.alpha > 10:
                self.alpha -= 10

        print(self.alpha)


if __name__ == '__main__':
    screen = pygame.display.set_mode(resolution)
    game = DayNight(screen)
    game.run()
