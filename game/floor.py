import pygame

from config import config

class Floor:
    def __init__(self, y: int):
        assert isinstance(y, int) and y > 0, "y musi być dodatnią liczbą całkowitą"

        self.floor_y_ratio = y / config.SCREEN_HEIGHT
        self.floor_y = y

        self.outer_rect = pygame.Rect(0, self.floor_y, config.SCREEN_WIDTH, config.FLOOR_OUTER_HEIGHT)
        self.outer_rect.centerx = config.SCREEN_WIDTH // 2

        self.inner_rect = pygame.Rect(0, self.floor_y, config.SCREEN_WIDTH, config.SCREEN_HEIGHT - self.floor_y)
        self.inner_rect.centerx = config.SCREEN_WIDTH // 2

    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.rect(screen, config.FLOOR_INNER_COLOR, self.inner_rect)
        pygame.draw.rect(screen, config.FLOOR_OUTER_COLOR, self.outer_rect)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        self.floor_y = int(screen_height * self.floor_y_ratio)

        outer_height = int (screen_height * (config.FLOOR_OUTER_HEIGHT / config.SCREEN_HEIGHT))

        self.outer_rect = pygame.Rect(0, self.floor_y, screen_width, outer_height)
        self.outer_rect.centerx = screen_width // 2

        inner_height = screen_height - self.floor_y

        self.inner_rect = pygame.Rect(0, self.floor_y, screen_width, inner_height)
        self.inner_rect.centerx = screen_width // 2

    def get_screen_floor_y(self, screen: pygame.Surface) -> int:
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        screen_height = screen.get_height()
        return int(screen_height * self.floor_y_ratio)