import pygame

from config import config

class Slider:
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 min_val: int, max_val: int,
                 start_val: int,
                 color: tuple[int, int, int] = config.BUTTON_COLOR):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(min_val, (int, float)), "min_val musi być liczbą"
        assert isinstance(max_val, (int, float)), "max_val musi być liczbą"
        assert isinstance(start_val, (int, float)), "start_val musi być liczbą"
        assert min_val < max_val, "min_val musi być mniejsze niż max_val"
        assert min_val <= start_val <= max_val, "start_val musi być w zakresie min_val i max_val"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.color = color
        self.inner_color = tuple(min(255, int(c * 1.2)) for c in self.color)

        self.slider_size = self.height * 0.6
        self.dragging = False

        self.relative_position = (start_val - min_val) / (max_val - min_val)

        self.outer_rect = pygame.Rect(0, 0, self.width, self.height)
        self.inner_rect = pygame.Rect(0, 0, self.width, self.height)
        self.slider_rect = pygame.Rect(0, 0, self.slider_size, self.slider_size)

    def draw(self, screen: pygame.Surface):
        self._validate_draw_params(screen)

        self._update_size(screen)

        pygame.draw.rect(screen, self.color, self.outer_rect, border_radius=4)
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, border_radius=4)
        pygame.draw.rect(screen, config.SLIDER_COLOR, self.slider_rect, border_radius=4)

    def is_hovered(self, mouse_position):
        assert isinstance(mouse_position, tuple) and len(mouse_position) == 2, "mouse_position musi być krotką (x, y)"
        return self.slider_rect.collidepoint(mouse_position)

    def handle_event(self, event):
        assert isinstance(event, pygame.event.EventType), "event musi być instancją pygame.event.EventType"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()

            min_x = self.outer_rect.left + self.slider_rect.width // 2 + 10
            max_x = self.outer_rect.right - self.slider_rect.width // 2 - 10

            clamped_x = max(min_x, min(mouse_x, max_x))
            self.relative_position = (clamped_x - min_x) / (max_x - min_x)
            self.value = self.min_val + self.relative_position * (self.max_val - self.min_val)

    def _update_size(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        scale_x = screen_width / config.SCREEN_WIDTH
        scale_y = screen_height / config.SCREEN_HEIGHT

        outer_width = int(self.width * scale_x)
        outer_height = int(self.height * scale_y)
        slider_size_scaled = int(self.slider_size * scale_y)

        center_x = int(self.x * scale_x)
        center_y = int(self.y * scale_y)

        self.outer_rect = pygame.Rect(0, 0, outer_width, outer_height)
        self.outer_rect.center = (center_x, center_y)

        self.inner_rect = pygame.Rect(0, 0, outer_width - slider_size_scaled, outer_height - slider_size_scaled)
        self.inner_rect.center = (center_x, center_y)

        min_x = self.outer_rect.left + slider_size_scaled // 2 + 10
        max_x = self.outer_rect.right - slider_size_scaled // 2 - 10

        slider_x = int(min_x + self.relative_position * (max_x - min_x))
        slider_y = self.outer_rect.centery

        self.slider_rect = pygame.Rect(0, 0, slider_size_scaled, slider_size_scaled)
        self.slider_rect.center = (slider_x, slider_y)

    @staticmethod
    def _validate_draw_params(screen: pygame.Surface):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")