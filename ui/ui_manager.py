import pygame

from config import config
from config.enums import WindowState

from game.player import Player
from game.floor import Floor
from game.engine import Engine
from game.level_editor import LevelEditor

from ui.label import Label
from ui.button import Button
from ui.text_input_field import TextInputField
from ui.checkbox import Checkbox

class UIManager:
    def __init__(self):
        self.window = None

        # [MENU]
        self.menu_components = []

        self.title_label = None
        self.title_description_label = None
        self.start_button = None
        self.level_editor_button = None
        self.exit_button = None

        # [PAUSE]
        self.pause_components = []

        self.title_pause_label = None
        self.resume_button = None
        self.back_pause_button = None

        # [GAME]
        self.game_components = []
        self.coordinate_x_label = None
        self.coordinate_y_label = None
        self.floor_y_label = None

        # [SELECT]
        self.select_components = []

        self.current_level = None
        self.current_page_select = 1
        self.select_title_label = None
        self.select_page_label = None
        self.level_button = None
        self.levels = None

        # [EDIT CONFIRM]
        self.edit_components = []

        self.edit_confirm_title_label = None
        self.edit_confirm_yes_button = None
        self.edit_confirm_no_button = None

        # [SAVE PROMPT]
        self.save_components = []

        self.save_prompt_title_label = None

        self.level_name_title_label = None
        self.level_name_input_field = None

        self.difficulty_name_title_label = None
        self.difficulty_name_input_field = None

        self.save_prompt_save_button = None
        self.save_prompt_cancel_button = None

        # [LOAD PROMPT]
        self.load_components = []

        self.current_page_load = 1
        self.load_page_label = None

        self.load_prompt_title_label = None

        self.load_prompt_back_button = None

        self.list_left_load_prompt_button = None
        self.list_right_load_prompt_button = None

        self.filter_title_label = None
        self.filter_easy_checkbox = None
        self.filter_normal_checkbox = None
        self.filter_hard_checkbox = None

        self.level_info_buttons = []

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

    def init(self, levels):

        self.levels = levels

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.menu_view_init()
        self.pause_view_init()
        self.game_view_init()
        self.level_select_init()
        self.edit_confirm_view_init()
        self.save_prompt_init()
        self.load_prompt_init()

    def menu_view_init(self):
        self.title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 235,
            "Jump Game", 240)

        self.title_description_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 95,
            "By s31230", 64)

        self.start_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            220, 80, "Start")

        self.level_editor_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 100,
            220, 80, "Editor")

        self.exit_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 200,
            220, 80, "Exit")

        self.menu_components = [self.title_label, self.title_description_label, self.start_button, self.level_editor_button, self.exit_button]

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

        self.pause_components = [self.title_pause_label, self.resume_button, self.back_pause_button]

    def game_view_init(self):
        self.coordinate_x_label = Label(
            100, 100, "")

        self.coordinate_y_label = Label(
            250, 100, "")

        self.floor_y_label = Label(
            430, 100, "")

        self.game_components = [self.coordinate_x_label, self.coordinate_y_label, self.floor_y_label]

    def level_select_init(self):
        self.select_title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 340,
            "Select level", 200)

        self.select_page_label = Label(
            self.screen_width // 2, 850, f"Page {self.current_page_select}")

        self.create_level_button()

        self.select_components = [self.select_title_label, self.select_page_label]

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

        self.edit_components = [self.edit_confirm_title_label, self.edit_confirm_yes_button, self.edit_confirm_no_button]

    def save_prompt_init(self):
        self.save_prompt_title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 185,
            "Save level as", 200)

        # [NAME]
        self.level_name_title_label = Label(
            self.screen_width // 2 - 380, self.screen_height // 2,
            "Name", 72)

        self.level_name_input_field = TextInputField(
            self.screen_width // 2, self.screen_height // 2,
            500, 80, "")

        # [DIFFICULTY]
        self.difficulty_name_title_label = Label(
            self.screen_width // 2 - 380, self.screen_height // 2 + 100,
            "Difficulty", 72)

        self.difficulty_name_input_field = TextInputField(
            self.screen_width // 2, self.screen_height // 2 + 100,
            500, 80, "")

        # [DIALOG OPTIONS]
        self.save_prompt_save_button = Button(
            self.screen_width // 2 - 120, self.screen_height // 2 + 300,
            220, 80, "Save")

        self.save_prompt_cancel_button = Button(
            self.screen_width // 2 + 120, self.screen_height // 2 + 300,
            220, 80, "Cancel")

        self.save_components = \
            [self.save_prompt_title_label,
             self.level_name_title_label, self.level_name_input_field,
             self.difficulty_name_title_label, self.difficulty_name_input_field,
             self.save_prompt_save_button, self.save_prompt_cancel_button]

    def load_prompt_init(self):
        self.load_page_label = Label(
            self.screen_width // 2, 850, f"Page {self.current_page_load}")

        self.load_prompt_title_label = Label(
            self.screen_width // 2, self.screen_height // 2 - 340,
            "Select level", 200)

        self.load_prompt_back_button = Button(
            self.screen_width // 2, self.screen_height // 2 + 300,
            220, 80, "Cancel")

        self.list_left_load_prompt_button = Button(
            self.screen_width // 2 - 160, self.screen_height // 2 + 300,
            80, 80, "<")

        self.list_right_load_prompt_button = Button(
            self.screen_width // 2 + 160, self.screen_height // 2 + 300,
            80, 80, ">")

        self.filter_title_label = Label(
            150, 300, "Filters:", 96)

        self.filter_easy_checkbox = Checkbox(
            110, 370, 50, "Easy", True)

        self.filter_normal_checkbox = Checkbox(
            110, 440, 50, "Normal", True)

        self.filter_hard_checkbox = Checkbox(
            110, 510, 50, "Hard", True)

        self.create_level_load_buttons()

        self.load_components = \
            [self.load_page_label, self.load_prompt_title_label,
             self.load_prompt_back_button, self.list_left_load_prompt_button, self.list_right_load_prompt_button,
             self.filter_title_label,
             self.filter_easy_checkbox, self.filter_normal_checkbox, self.filter_hard_checkbox]

    def create_level_load_buttons(self):
        self.level_info_buttons.clear()

        filtered_levels = self.levels_filtered()

        levels_per_page = config.LEVELS_PER_PAGE
        start_index = (self.current_page_load - 1) * levels_per_page
        end_index = start_index + levels_per_page

        visible_levels = filtered_levels[start_index:end_index]

        button_width, button_height = (config.LEVEL_LOAD_BUTTON_WIDTH, config.LEVEL_LOAD_BUTTON_HEIGHT)
        padding = config.PADDING

        total_width = button_width * 3 + padding * 2
        total_height = button_height * 2 + padding

        start_x = self.screen_width // 2 - total_width // 2 + button_width // 2
        start_y = self.screen_height // 2 - total_height // 2 + button_height // 2

        for index, level in enumerate(visible_levels):
            row = index // 3
            column = index % 3

            x = int(start_x + column * (button_width + padding))
            y = int(start_y + row * (button_height + padding))

            button = Button(
                x, y, button_width, button_height,
                level["name"],
                config.BUTTON_COLOR,
                config.TEXT_COLOR,
                config.FONT_SIZE,
                level["difficulty"])

            self.level_info_buttons.append((button, level))

    def levels_filtered(self):
        return [level for level in self.levels if (
                    (level["difficulty"] == "easy" and self.filter_easy_checkbox.checked) or
                    (level["difficulty"] == "normal" and self.filter_normal_checkbox.checked) or
                    (level["difficulty"] == "hard" and self.filter_hard_checkbox.checked))
        ]

    def change_level_load_page(self, direction):
        if direction == "left":
            if self.current_page_load > 1:
                self.current_page_load -= 1
                self.create_level_load_buttons()
                self.load_page_label.set_text(f"Page {self.current_page_load}")
        elif direction == "right":
            if self.current_page_load < ((len(self.levels_filtered()) - 1) // 6) + 1:
                self.current_page_load += 1
                self.create_level_load_buttons()
                self.load_page_label.set_text(f"Page {self.current_page_load}")

    def create_level_button(self):
        self.current_level = None

        for level in self.levels:
            if int(level["index"]) == int(self.current_page_select):
                self.current_level = level

        screen_width, screen_height = self.window.get_size()

        button_width = int(screen_width * 0.8)
        button_height = int(screen_height * 0.8)

        self.level_button = Button(
            self.screen_width // 2, self.screen_height // 2,
            int(button_width * 0.7), int(button_height * 0.7), self.current_level["name"],
            config.BUTTON_COLOR, config.TEXT_COLOR, 128, self.current_level["difficulty"])

    def change_level_select_page(self, direction):
        if direction == "left":
            if self.current_page_select > 1:
                self.current_page_select -= 1
                self.create_level_button()
                self.select_page_label.set_text(f"Page {self.current_page_select}")
        elif direction == "right":
            if self.current_page_select < len(self.levels):
                self.current_page_select += 1
                self.create_level_button()
                self.select_page_label.set_text(f"Page {self.current_page_select}")

    def game_components_render(self, player: Player, floor: Floor, level_editor: LevelEditor, engine: Engine):
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"
        assert isinstance(level_editor, LevelEditor), "level_editor musi być instancją klasy LevelEditor"

        engine.draw_objects(self.window)
        player.draw(self.window, floor, engine.camera_offset_x)
        floor.draw(self.window)

        for component in self.game_components:
            component.draw(self.window)

        self.coordinate_x_label.set_text(f"x={player.x:.2f}")
        self.coordinate_y_label.set_text(f"y={player.y:.2f}")
        self.floor_y_label.set_text(f"x={floor.floor_y}")

        engine.attempt_counter_label.x = engine.camera_offset_x + 400
        engine.attempt_counter_label.set_text(f"Attempt {engine.attempts}")
        engine.attempt_counter_label.draw(self.window)

    def render(self, window_state: WindowState, player: Player, floor: Floor, level_editor: LevelEditor, engine: Engine):
        assert isinstance(window_state, WindowState), "window_state musi być obiektem instancji WindowState"
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"
        assert isinstance(level_editor, LevelEditor), "level_editor musi być instancją klasy LevelEditor"

        if window_state == WindowState.MENU:
            self.window.fill(config.BACKGROUND_COLOR)

            for component in self.menu_components:
                component.draw(self.window)

        if window_state == WindowState.GAME:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            self.game_components_render(player, floor, level_editor, engine)

        if window_state == WindowState.PAUSE:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            self.game_components_render(player, floor, level_editor, engine)

            transparent_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            transparent_surface.fill(config.BACKGROUND_PAUSE_COLOR)
            self.window.blit(transparent_surface, (0, 0))

            for component in self.pause_components:
                component.draw(self.window)

        if window_state == WindowState.SELECT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            for component in self.select_components:
                component.draw(self.window)

            self.level_button.draw(self.window)

        if window_state == WindowState.EDIT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))
            level_editor.render()

        if window_state == WindowState.EDIT_CONFIRM:
            self.window.fill(tuple(int(c * 1.2) for c in config.BACKGROUND_COLOR))
            level_editor.render()

            transparent_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
            transparent_surface.fill(config.BACKGROUND_PAUSE_COLOR)

            self.window.blit(transparent_surface, (0, 0))

            for component in self.edit_components:
                component.draw(self.window)

        if window_state == WindowState.SAVE_PROMPT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            for component in self.save_components:
                component.draw(self.window)

        if window_state == WindowState.LOAD_PROMPT:
            self.window.fill(tuple(int(c * 0.8) for c in config.BACKGROUND_COLOR))

            for component in self.load_components:
                component.draw(self.window)

            for level_button, level in self.level_info_buttons:
                level_button.draw(self.window)

        pygame.display.update()