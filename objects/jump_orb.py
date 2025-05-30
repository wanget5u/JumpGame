import pygame

from config import config

class JumpOrb:
    def __init__(self, x: int, y: int):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"

        self.x = x
        self.y = y
        self.outer_diameter = config.ORB_OUTER_DIAMETER
        self.inner_diameter = config.ORB_INNER_DIAMETER

        self.outer_color = config.ORB_OUTER_COLOR
        self.inner_color = config.ORB_INNER_COLOR

        self.outer_radius = self.outer_diameter // 2
        self.inner_radius = self.inner_diameter // 2

        self.screen_x = self.x
        self.screen_y = self.y

    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.circle(screen, self.outer_color, (self.screen_x, self.screen_y), self.outer_radius, 2)
        pygame.draw.circle(screen, self.inner_color, (self.screen_x, self.screen_y), self.inner_radius)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        self.outer_radius = int((screen_width * self.outer_diameter / config.SCREEN_WIDTH) / 2)
        self.inner_radius = int((screen_height * self.inner_diameter / config.SCREEN_HEIGHT) / 2)

        self.screen_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        self.screen_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))