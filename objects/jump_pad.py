import pygame

from config import config

class JumpPad:
    def __init__(self, x: int, y: int):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"

        self.x = x
        self.y = y

        self.outer_color = config.PAD_OUTER_COLOR
        self.outer_width = config.PAD_OUTER_WIDTH
        self.outer_height = config.PAD_OUTER_HEIGHT
        self.outer_rect = pygame.Rect(0, y + config.BLOCK_OUTER_SIZE - self.outer_height, self.outer_width, self.outer_height)
        self.outer_rect.centerx = self.x

        self.inner_color = config.PAD_INNER_COLOR
        self.inner_width = config.PAD_INNER_WIDTH
        self.inner_height = config.PAD_INNER_HEIGHT
        self.inner_rect = pygame.Rect(0, y + config.BLOCK_OUTER_SIZE - self.inner_height, self.inner_width, self.inner_height)
        self.inner_rect.centerx = self.x

    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.rect(screen, self.outer_color, self.outer_rect)
        pygame.draw.rect(screen, self.inner_color, self.inner_rect)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        rect_outer_width = int(screen_width * (self.outer_width / config.SCREEN_WIDTH))
        rect_outer_height = int(screen_height * (self.outer_height / config.SCREEN_HEIGHT))

        rect_inner_width = int(screen_width * (self.inner_width / config.SCREEN_WIDTH))
        rect_inner_height = int(screen_height * (self.inner_height / config.SCREEN_HEIGHT))

        rect_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        outer_rect_y = int(screen_height * ((self.y + config.BLOCK_OUTER_SIZE // 2 - rect_outer_height) / config.SCREEN_HEIGHT))
        inner_rect_y = int(screen_height * ((self.y + config.BLOCK_OUTER_SIZE // 2 - rect_inner_height) / config.SCREEN_HEIGHT))

        self.outer_rect = pygame.Rect(0, outer_rect_y, rect_outer_width, rect_outer_height)
        self.outer_rect.centerx = rect_x

        self.inner_rect = pygame.Rect(0, inner_rect_y, rect_inner_width, rect_inner_height)
        self.inner_rect.centerx = rect_x