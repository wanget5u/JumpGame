import pygame

from config import config

class EndWall:
    def __init__(self, x: int):
        assert isinstance(x, int) and x > 0, "x musi być dodatnią liczbą całkowitą"

        self.initial_wall_x = x
        self.wall_x = x
        self.outer_rect = pygame.Rect(x, 0, config.END_WALL_OUTER_WIDTH, config.SCREEN_HEIGHT)
        self.inner_rect = pygame.Rect(x, 0, 0, config.SCREEN_HEIGHT)

    def draw(self, screen: pygame.Surface):
        self._validate_draw_params(screen)

        self._update_size(screen)

        pygame.draw.rect(screen, config.END_WALL_INNER_COLOR, self.inner_rect)
        pygame.draw.rect(screen, config.END_WALL_OUTER_COLOR, self.outer_rect)

    def _update_size(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        outer_width = int(config.END_WALL_OUTER_WIDTH * (screen_width / config.SCREEN_WIDTH))
        self.outer_rect = pygame.Rect(self.wall_x, 0, outer_width, screen_height)

        inner_width = screen_width - self.wall_x
        self.inner_rect = pygame.Rect(self.wall_x, 0, inner_width, screen_height)

    @staticmethod
    def _validate_draw_params(screen: pygame.Surface):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")