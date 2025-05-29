import pygame

from config import config

class TextInputField:
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 text: str,
                 color: tuple[int, int, int] = config.BUTTON_COLOR,
                 text_color: tuple[int, int, int] = config.TEXT_COLOR,
                 max_length: int = 18,
                 text_size: int = config.FONT_SIZE):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all( 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(max_length, int) and max_length > 0, "max_length musi być dodatnią liczbą całkowitą"
        assert isinstance(text_size, int) and text_size > 0, "text_size musi być nieujemną liczbą całkowitą"

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        self.color_inactive = color
        self.color = self.color_inactive
        self.color_active = tuple(min(255, int(c * 1.5)) for c in color)

        self.text = text
        self.text_size = text_size
        self.font = pygame.font.SysFont(None, int(text_size))
        self.text_color = text_color
        self.max_length = max_length
        self.active = False

    def draw(self, screen: pygame.Surface):
        self._validate_draw_params(screen)

        self._update_size(screen)

        txt_surface = self.font.render(self.text, True, self.text_color)
        text_rect = txt_surface.get_rect(center=self.rect.center)
        screen.blit(txt_surface, text_rect)
        pygame.draw.rect(screen, self.color, self.rect, 5)

    def _update_size(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        rect_width = int(self.width * (screen_width / config.SCREEN_WIDTH))
        rect_height = int(self.height * (screen_height / config.SCREEN_HEIGHT))
        rect_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.rect = pygame.Rect(0, 0, rect_width, rect_height)
        self.rect.center = (rect_x, rect_y)
        self.font = pygame.font.SysFont(None, int(self.text_size))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_DELETE:
                self.text = ""
            elif len(self.text) < self.max_length and event.unicode.isalnum():
                self.text += event.unicode

    @staticmethod
    def _validate_draw_params(screen: pygame.Surface):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")