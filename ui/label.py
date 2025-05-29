import pygame.font

from config import config

class Label:
    def __init__(self,
                 x: int, y: int,
                 text: str,
                 text_size: int = config.FONT_SIZE,
                 text_color: tuple[int, int, int] = config.TEXT_COLOR):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(text_size, (int, float)) and text_size > 0, "font_size musi być dodatnią liczbą"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        self.x = x
        self.y = y
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.font = pygame.font.SysFont(None, int(text_size))

        self.rel_x = x
        self.rel_y = y

    """Rysowanie tekstu na ekranie."""
    def draw(self, screen):
        self._validate_draw_params(screen)

        self._update_size(screen)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rel_x, self.rel_y))
        screen.blit(text_surface, text_rect)

    """Aktualizacja wielkości guzika względem dynamicznie zmieniającej się rozdzielczości okna."""

    def _update_size(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        self.rel_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        self.rel_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        text_size = int(int(screen_width * (self.text_size / config.SCREEN_WIDTH)) * 0.8)
        self.font = pygame.font.SysFont(None, max(24, text_size))

    """Ustawienie tekstu labelu."""
    def set_text(self, text: str):
        self._validate_set_text(text)
        self.text = text

    @staticmethod
    def _validate_draw_params(screen: pygame.Surface):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")

    @staticmethod
    def _validate_set_text(text: str):
        if not isinstance(text, str):
            raise ValueError("tekst musi być typu str")