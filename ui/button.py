import pygame

from config import config

class Button:
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 text: str,
                 color: tuple[int, int, int] = config.BUTTON_COLOR,
                 text_color: tuple[int, int, int] = config.TEXT_COLOR,
                 text_size: int = config.FONT_SIZE):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_size, int) and text_size > 0, "text_size musi być nieujemną liczbą całkowitą"

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)

        self.text = text
        self.color = color
        self.color_hover = tuple(min(255, int(c * 1.2)) for c in color)  # Kolor przy najechaniu kursorem
        self.color_click = tuple(min(255, int(c * 1.4)) for c in color)  # Kolor przy kliknięciu
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.SysFont(None, int(text_size))

        self.is_pressed = False

    """Rysowanie przycisku na ekranie."""
    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        if self.is_pressed:
            current_color = self.color_click
        elif self.is_hovered():
            current_color = self.color_hover
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=4)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    """Aktualizacja wielkości guzika względem dynamicznie zmieniającej się rozdzielczości okna."""
    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        rect_width = int(screen_width * (self.width / config.SCREEN_WIDTH))
        rect_height = int(screen_height * (self.height / config.SCREEN_HEIGHT))
        rect_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.rect = pygame.Rect(0, 0, rect_width, rect_height)
        self.rect.center = (rect_x, rect_y)
        self.font = pygame.font.SysFont(None, int(self.text_size))

    """Sprawdzanie, czy kursor znajduje się nad przyciskiem."""
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    """Obsługa zdarzeń myszy dla przycisku."""
    def handle_event(self, event, on_click_event: callable):
        assert callable(on_click_event), "on_click_event musi być callable"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered():
            self.is_pressed = True

        elif event.type == pygame.MOUSEMOTION and not self.is_hovered():
            self.is_pressed = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered():
                on_click_event()
            self.is_pressed = False