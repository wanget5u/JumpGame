import pygame

from config import config
from config.enums import WindowState

from game.player import Player
from game.floor import Floor

from ui.label import Label
from ui.button import Button

class UIManager:
    def __init__(self):
        self.window = None

        self.title_label = None
        self.title_description_label = None
        self.start_button = None

        self.title_pause_label = None
        self.resume_button = None
        self.back_pause_button = None

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

    def init(self):
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.menu_init()
        self.pause_init()

    def menu_init(self):
        self.title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 235,
            "Jump Game", 240)

        self.title_description_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 95,
            "By s31230", 64)

        self.start_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            220, 80,"Start")

    def pause_init(self):
        self.title_pause_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 185,
            "Pause", 200)

        self.resume_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            220, 80, "Resume")

        self.back_pause_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 95,
            320, 80, "Back to Title")

    def render(self, window_state: WindowState, player: Player, floor: Floor):
        assert isinstance(window_state, WindowState), "window_state musi być obiektem instancji WindowState"
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"

        if window_state == WindowState.MENU:
            self.window.fill(config.BACKGROUND_COLOR)

            self.title_label.draw(self.window)
            self.title_description_label.draw(self.window)
            self.start_button.draw(self.window)

        if window_state == WindowState.GAME:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            player.draw(self.window)
            floor.draw(self.window)

        if window_state == WindowState.PAUSE:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            player.draw(self.window)
            floor.draw(self.window)

            transparent_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            transparent_surface.fill(config.BACKGROUND_PAUSE_COLOR)

            self.window.blit(transparent_surface, (0, 0))

            self.title_pause_label.draw(self.window)
            self.resume_button.draw(self.window)
            self.back_pause_button.draw(self.window)

        pygame.display.update()