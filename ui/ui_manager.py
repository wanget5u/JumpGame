import pygame

from config import config
from config.enums import WindowState

from game.player import Player
from game.floor import Floor

from game.level_editor import LevelEditor

from ui.label import Label
from ui.button import Button

class UIManager:
    def __init__(self):
        self.window = None

        # [MENU]
        self.title_label = None
        self.title_description_label = None
        self.start_button = None
        self.level_editor_button = None
        self.exit_button = None

        # [PAUSE]
        self.title_pause_label = None
        self.resume_button = None
        self.back_pause_button = None

        # [GAME]
        self.coordinate_x_label = None
        self.coordinate_y_label = None
        self.floor_y_label = None

        # [SELECT]
        self.current_page = 1
        self.page_label = None
        self.level_button = None
        self.levels = None

        # [EDIT CONFIRM]
        self.edit_confirm_title_label = None
        self.edit_confirm_yes_button = None
        self.edit_confirm_no_button = None

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

    def init(self, levels: list):
        assert isinstance(levels, list), "levels musi być listą"

        self.levels = levels

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.menu_view_init()
        self.pause_view_init()
        self.game_view_init()
        self.level_select_init()
        self.edit_confirm_view_init()

    def menu_view_init(self):
        self.title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 235,
            "Jump Game", 240)

        self.title_description_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 95,
            "By s31230", 64)

        self.start_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            220, 80,"Start")

        self.level_editor_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 100,
            220, 80, "Editor")

        self.exit_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 200,
            220, 80, "Exit")

    def pause_view_init(self):
        self.title_pause_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 185,
            "Pause", 200)

        self.resume_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            220, 80, "Resume")

        self.back_pause_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 95,
            320, 80, "Back to Title")

    def game_view_init(self):
        self.coordinate_x_label = Label(
            100, 100, "")

        self.coordinate_y_label = Label(
            250, 100, "")

        self.floor_y_label = Label(
            430, 100, "")

    def level_select_init(self):
        self.page_label = Label(
            self.screen_width // 2, 850, f"Page {self.current_page}")

        self.create_level_button()

    def create_level_button(self):
        current_level = None

        for level in self.levels:
            if int(level["index"]) == int(self.current_page):
                current_level = level

        screen_width, screen_height = self.window.get_size()

        button_width = int(screen_width * 0.8)
        button_height = int(screen_height * 0.8)

        self.level_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            button_width, button_height, current_level["name"],
            config.BUTTON_COLOR, config.TEXT_COLOR, 128)

    def change_level_select_page(self, direction):
        if direction == "left":
            if self.current_page > 1:
                self.current_page -= 1
                self.create_level_button()
                self.page_label.set_text(f"Page {self.current_page}")
        elif direction == "right":
            if self.current_page < len(self.levels):
                self.current_page += 1
                self.create_level_button()
                self.page_label.set_text(f"Page {self.current_page}")

    def edit_confirm_view_init(self):
        self.edit_confirm_title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 185,
            "Do you want to quit without saving?", 100)

        self.edit_confirm_yes_button = Button(
            self.screen_width // 2 - 120, self.screen_height // 2,
            220, 80, "Yes")

        self.edit_confirm_no_button = Button(
            self.screen_width // 2 + 120, self.screen_height // 2,
            220, 80, "No")

    def render(self, window_state: WindowState, player: Player, floor: Floor, level_editor: LevelEditor):
        assert isinstance(window_state, WindowState), "window_state musi być obiektem instancji WindowState"
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"
        assert isinstance(level_editor, LevelEditor), "level_editor musi być instancją klasy LevelEditor"

        if window_state == WindowState.MENU:
            self.window.fill(config.BACKGROUND_COLOR)

            self.title_label.draw(self.window)
            self.title_description_label.draw(self.window)
            self.start_button.draw(self.window)
            self.level_editor_button.draw(self.window)
            self.exit_button.draw(self.window)

        if window_state == WindowState.GAME:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            player.draw(self.window, floor)
            floor.draw(self.window)

            self.coordinate_x_label.set_text(f"x={player.x:.2f}")
            self.coordinate_x_label.draw(self.window)

            self.coordinate_y_label.set_text(f"y={player.outer_rect.bottom:.2f}")
            self.coordinate_y_label.draw(self.window)

            self.floor_y_label.set_text(f"floor_y={floor.floor_y:.2f}")
            self.floor_y_label.draw(self.window)

        if window_state == WindowState.PAUSE:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            player.draw(self.window, floor)
            floor.draw(self.window)

            transparent_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            transparent_surface.fill(config.BACKGROUND_PAUSE_COLOR)

            self.window.blit(transparent_surface, (0, 0))

            self.title_pause_label.draw(self.window)
            self.resume_button.draw(self.window)
            self.back_pause_button.draw(self.window)

        if window_state == WindowState.SELECT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            self.level_button.draw(self.window)
            self.page_label.draw(self.window)

        if window_state == WindowState.EDIT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            level_editor.render()

        if window_state == WindowState.EDIT_CONFIRM:
            self.window.fill(tuple(int(c * 1.2) for c in config.BACKGROUND_COLOR))

            level_editor.render()

            transparent_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            transparent_surface.fill(config.BACKGROUND_PAUSE_COLOR)

            self.window.blit(transparent_surface, (0, 0))

            self.edit_confirm_title_label.draw(self.window)
            self.edit_confirm_yes_button.draw(self.window)
            self.edit_confirm_no_button.draw(self.window)

        pygame.display.update()