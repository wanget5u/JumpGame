import pygame

from config import config
from config.enums import WindowState

from ui.button import Button

class UIManager:
    def __init__(self):
        self.window = None

        self.title_label = None
        self.start_button = None

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

        self.init()

    def init(self):
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), config.FULLSCREEN)

        self.menu_init()

    def menu_init(self):
        self.start_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            180, 60,"Start")

    def render(self, window_state: WindowState):
        assert isinstance(window_state, WindowState), "window_state musi być obiektem instancji WindowState"

        if window_state == window_state.MENU:
            self.window.fill(config.BACKGROUND_COLOR)

            self.start_button.draw(self.window)

        if window_state == window_state.GAME:
            self.window.fill(tuple(int(c * 0.6) for c in config.BACKGROUND_COLOR))

        pygame.display.update()