import pygame

from config import config

class Checkbox:
    def __init__(self,
                 x: int, y: int,
                 size: int,
                 text: str,
                 checked: bool = False,
                 color: tuple[int, int, int] = config.BUTTON_COLOR,
                 text_color: tuple[int, int, int] = config.TEXT_COLOR,
                 text_size: int = config.FONT_SIZE):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(size, int) and size > 0, "size musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(checked, bool), "checked musi być wartością boolowską"
        assert all(isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color) for color in [color, text_color]), "kolory muszą być krotkami 3 liczb całkowitych z zakresu 0-255"

        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)

        self.text = text
        self.color = color
        self.color_hover = tuple(min(255, int(c * 1.2)) for c in color)
        self.color_click = tuple(min(255, int(c * 1.4)) for c in color)
        self.check_color = tuple(int(x * 2.4) for x in color)

        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.SysFont(None, int(self.text_size))
        self.scaled_text_size = None

        self.checked = checked
        self.is_pressed = False

    """Rysowanie checkboxa i tekstu na ekranie."""
    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        if self.is_pressed:
            current_color = self.color_click
        elif self.is_hovered():
            current_color = self.color_hover
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=4)

        if self.checked:
            inner_rect = self.rect.inflate(-self.rect.width * 0.4, -self.rect.height * 0.4)
            pygame.draw.rect(screen, self.check_color, inner_rect, border_radius=3)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 20, self.rect.centery))
        screen.blit(text_surface, text_rect)

    """Sprawdzanie, czy kursor znajduje się nad checkboxem."""
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    """Obsługa zdarzeń myszy dla checkboxa."""
    def handle_event(self, event, on_toggle=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered():
            self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered():
                self.checked = not self.checked

                if callable(on_toggle):
                    on_toggle()
            self.is_pressed = False

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        checkbox_size = int(screen_width * (self.size / config.SCREEN_WIDTH))

        rect_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.rect = pygame.Rect(0, 0, checkbox_size, checkbox_size)
        self.rect.center = (rect_x, rect_y)

        self.scaled_text_size = int(screen_height * (self.text_size / config.SCREEN_HEIGHT))
        self.font = pygame.font.SysFont(None, self.scaled_text_size)