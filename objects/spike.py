import pygame

from config import config

class Spike:
    def __init__(self, x: int, y: int):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"

        self.x = x
        self.y = y

        self.outer_width = config.SPIKE_OUTER_WIDTH
        self.outer_height = config.SPIKE_OUTER_HEIGHT
        self.inner_width = config.SPIKE_INNER_WIDTH
        self.inner_height = config.SPIKE_INNER_HEIGHT

        self.outer_color = config.SPIKE_OUTER_COLOR
        self.inner_color = config.SPIKE_INNER_COLOR

        self.outer_points = []
        self.inner_points = []

    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.polygon(screen, self.outer_color, self.outer_points)
        pygame.draw.polygon(screen, self.inner_color, self.inner_points)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        scale_x = screen_width / config.SCREEN_WIDTH
        scale_y = screen_height / config.SCREEN_HEIGHT

        x = int(self.x * scale_x)
        y = int(self.y * scale_y)

        outer_width = int(self.outer_width * scale_x)
        outer_height = int(self.outer_height * scale_y)

        self.outer_points = [
            (x, y - outer_height // 2),
            (x - outer_width // 2, y + outer_height // 2),
            (x + outer_width // 2, y + outer_height // 2)
        ]

        inner_width = int(self.inner_width * scale_x)
        inner_height = int(self.inner_height * scale_y)

        self.inner_points = [
            (x, y - inner_height // 2 + 2),
            (x + 2 - inner_width // 2, y + inner_height // 2),
            (x - 2 + inner_width // 2, y + inner_height // 2)
        ]

    def get_collision_rect(self):
        return pygame.Rect(self.outer_points[1][0], self.outer_points[0][1], self.outer_width, self.outer_height)

    def get_collision_points(self):
        return self.outer_points