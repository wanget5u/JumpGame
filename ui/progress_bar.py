import pygame

from config import config

class ProgressBar:
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 max_value: int,
                 color: tuple[int, int, int] = config.BUTTON_COLOR):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.inner_color = tuple(min(255, int(c * 2.4)) for c in self.color)

        self.value = 0
        self.max_value = max_value

        self.outer_rect = pygame.Rect(0, 0, self.width, self.height)
        self.progress_rect = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.rect(screen, self.color, self.outer_rect, border_radius=20)
        pygame.draw.rect(screen, self.inner_color, self.progress_rect, border_radius=20)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        scale_x = screen_width / config.SCREEN_WIDTH
        scale_y = screen_height / config.SCREEN_HEIGHT

        outer_width = int(self.width * scale_x)
        outer_height = int(self.height * scale_y)

        center_x = int(self.x * scale_x)
        center_y = int(self.y * scale_y)

        self.outer_rect = pygame.Rect(0, 0, outer_width, outer_height)
        self.outer_rect.center = (center_x, center_y)

        fill_percentage = self.value / self.max_value
        progress_width = int(outer_width * fill_percentage)

        self.progress_rect = pygame.Rect(
            self.outer_rect.left,
            self.outer_rect.top,
            progress_width,
            outer_height
        )

    def get_percentage(self):
        return (self.value / self.max_value) * 100