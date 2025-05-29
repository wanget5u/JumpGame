import json, os, pygame, pygame.event

from typing import Dict, Any, Optional

from pygame import VIDEORESIZE

from config import config
from config.enums import WindowState

from ui.ui_manager import UIManager

from game.level_editor import LevelEditor
from game.player import Player
from game.engine import Engine
from game.floor import Floor
from game.end_wall import EndWall

"""Zarządza ogólnym stanem, zdarzeniami, oraz koordynacją pomiędzy wszystkimi komponentami gry."""
class GameManager:
    def __init__(self):
        self.running = False
        self.window_state: Optional[WindowState] = None

        # [Game objects]
        self.floor: Optional[Floor] = None
        self.player: Optional[Player] = None
        self.levels: Dict[str, Any] = {}
        self.current_level: Optional[Dict[str, Any]] = None

        # [Managers]
        self.ui_manager: Optional[UIManager] = None
        self.engine: Optional[Engine] = None
        self.level_editor: Optional[LevelEditor] = None

        # [Handlers]
        self.handlers = {
            WindowState.MENU: self._handle_menu_events,
            WindowState.GAME: self._handle_game_events,
            WindowState.PAUSE: self._handle_pause_events,
            WindowState.SELECT: self._handle_select_events,
            WindowState.EDIT: self._handle_edit_events,
            WindowState.EDIT_CONFIRM: self._handle_edit_confirm_events,
            WindowState.SAVE_PROMPT: self._handle_save_prompt_events,
            WindowState.LOAD_PROMPT: self._handle_load_prompt_events,
            WindowState.LEVEL_COMPLETE: self._handle_level_complete_events,
        }

    """Inicjalizuje wszystkie komponenty gry oraz stan początkowy okna."""
    def init(self):
        self.load_levels()

        self.ui_manager = UIManager()
        self.ui_manager.init(self.levels)

        self.floor = Floor(config.FLOOR_Y)
        self.engine = Engine(self.floor)

        self.level_editor = LevelEditor(self.ui_manager.window, self.levels, self.floor)

        self.player = Player()
        self.engine.reset_player(self.player)

        self.window_state = WindowState.MENU
        self.running = True

    """Aktualizacja gry na podstawie obecnego stanu okna."""
    def update(self, delta_time: float):
        self._validate_delta_time(delta_time)

        if self.window_state == WindowState.GAME: self._update_game_state(delta_time)

        self.poll_events()

    def _update_game_state(self, delta_time: float):
        self._handle_player_input()
        self._update_ui_elements()
        self._check_level_completion()

        game_over = self.engine.update_player(self.player, delta_time, self.ui_manager.window)

        if game_over:
            self.engine.attempts += 1
            self.engine.reset_player(self.player)

    def _handle_player_input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_UP] or mouse_buttons[0]: self.engine.player_jump(self.player)

    def _update_ui_elements(self):
        self.ui_manager.progress_bar.value = self.player.x

        self.ui_manager.attempt_counter_label.x = self.engine.camera_offset_x + config.ATTEMPT_LABEL_X_OFFSET
        self.ui_manager.attempt_counter_label.set_text(f"Attempt {self.engine.attempts}")
        self.ui_manager.coordinate_x_label.set_text(f"x={self.player.x:.2f}")
        self.ui_manager.coordinate_y_label.set_text(f"y={self.player.y:.2f}")
        self.ui_manager.floor_y_label.set_text(f"x={self.floor.floor_y}")

        progress_percentage = self.ui_manager.progress_bar.get_percentage()
        self.ui_manager.progress_percentage_label.set_text(f"{progress_percentage:.2f} %")

    def _check_level_completion(self):
        if not self.engine.end_wall: return

        self.engine.end_wall.wall_x = ( self.engine.end_wall.initial_wall_x + self.engine.camera_offset_x)

        if self.player.x >= self.engine.end_wall.initial_wall_x:
            self.ui_manager.progress_bar.value = 0
            self.set_window_state(WindowState.LEVEL_COMPLETE)

    def level_start(self):
        self.current_level = self.ui_manager.current_level
        self.engine.reset_player(self.player)
        self.engine.set_objects_from_layout(self.current_level["layout"])
        self.engine.attempts = 1

        furthest_object_x = self.engine.get_furthest_object_x()
        self.ui_manager.progress_bar.max_value = furthest_object_x
        self.engine.end_wall = EndWall(furthest_object_x)

        self.set_window_state(WindowState.GAME)

    """Obsługuje wszystkie zdarzenia pygame w zależności od obecnego stanu okna."""
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            elif event.type == pygame.QUIT:
                self.game_quit()
            else:
                self._handle_state_specific_events(event)

    """Przekazanie wydarzenia do konkretnej metody odpowiedzialnej za obsługiwanie danego wydarzenia."""
    def _handle_state_specific_events(self, event):
        self.handlers.get(self.window_state)(event)

    def _handle_menu_events(self, event):
        self.ui_manager.start_button.handle_event(event, lambda: self.set_window_state(WindowState.SELECT))

        def level_editor_action():
            self.level_editor.current_level = self.level_editor.create_empty_level()
            self.set_window_state(WindowState.EDIT)

        self.ui_manager.level_editor_button.handle_event(event, level_editor_action)
        self.ui_manager.exit_button.handle_event(event, self.game_quit)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_quit()

    def _handle_game_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.PAUSE)

    def _handle_pause_events(self, event):
        self.ui_manager.resume_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))
        self.ui_manager.back_pause_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.GAME)

    def _handle_select_events(self, event):
        self.ui_manager.level_button.handle_event(event, self.level_start)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.ui_manager.change_level_select_page("left")
            elif event.key == pygame.K_RIGHT:
                self.ui_manager.change_level_select_page("right")
            elif event.key == pygame.K_ESCAPE:
                self.set_window_state(WindowState.MENU)

    def _handle_edit_events(self, event):
        def save_action():
            self.set_window_state(WindowState.SAVE_PROMPT)
            self.ui_manager.level_name_input_field.text = self.level_editor.current_level["name"]
            self.ui_manager.difficulty_name_input_field.text = self.level_editor.current_level["difficulty"]

        def load_action():
            self.set_window_state(WindowState.LOAD_PROMPT)

        def exit_action():
            if self.level_editor.is_saved:
                self.set_window_state(WindowState.MENU)
            else:
                self.set_window_state(WindowState.EDIT_CONFIRM)

        self.level_editor.handle_event(
            event=event,
            save_button_event=save_action,
            load_button_event=load_action,
            exit_button_event=exit_action
        )

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.EDIT_CONFIRM)

    def _handle_edit_confirm_events(self, event):
        self.ui_manager.edit_confirm_yes_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))
        self.ui_manager.edit_confirm_no_button.handle_event(event, lambda: self.set_window_state(WindowState.EDIT))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.EDIT)

    def _handle_save_prompt_events(self, event):
        def save_level():
            self.level_editor.current_level["name"] = self.ui_manager.level_name_input_field.text
            self.level_editor.current_level["difficulty"] = self.ui_manager.difficulty_name_input_field.text
            self.level_editor.save_levels()
            self.ui_manager.create_level_load_buttons()
            self.set_window_state(WindowState.MENU)

        self.ui_manager.save_prompt_save_button.handle_event(event, save_level)
        self.ui_manager.save_prompt_cancel_button.handle_event(event, lambda: self.set_window_state(WindowState.EDIT))

        self.ui_manager.level_name_input_field.handle_event(event)
        self.ui_manager.difficulty_name_input_field.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.EDIT)

    def _handle_load_prompt_events(self, event):
        self.ui_manager.load_prompt_back_button.handle_event(event, lambda: self.set_window_state(WindowState.EDIT))

        filter_action = lambda: self.ui_manager.create_level_load_buttons()
        self.ui_manager.filter_easy_checkbox.handle_event(event, filter_action)
        self.ui_manager.filter_normal_checkbox.handle_event(event, filter_action)
        self.ui_manager.filter_hard_checkbox.handle_event(event, filter_action)

        self.ui_manager.list_left_load_prompt_button.handle_event(event, lambda: self.ui_manager.change_level_load_page("left"))
        self.ui_manager.list_right_load_prompt_button.handle_event(event, lambda: self.ui_manager.change_level_load_page("right"))

        def load_level_action(level_data):
            self.level_editor.load_level(int(level_data["index"]))
            self.set_window_state(WindowState.EDIT)

        for button, level in self.ui_manager.level_info_buttons:
            button.handle_event(event, lambda l=level: load_level_action(l))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.ui_manager.change_level_load_page("left")
            elif event.key == pygame.K_RIGHT:
                self.ui_manager.change_level_load_page("right")
            elif event.key == pygame.K_ESCAPE:
                self.set_window_state(WindowState.EDIT)

    def _handle_level_complete_events(self, event):
        self.ui_manager.level_complete_back_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))
        self.ui_manager.level_complete_retry_button.handle_event(event, self.level_start)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.SELECT)

    def is_running(self) -> bool:
        return self.running

    def game_quit(self):
        self.running = False

    def render(self):
        self.ui_manager.render(
            self.window_state,
            self.player,
            self.floor,
            self.level_editor,
            self.engine
        )

    def set_window_state(self, window_state: WindowState):
        self._validate_window_state(window_state)
        self.window_state = window_state

    """Obsługuje zmianę wielkości okna zachowując współczynnik proporcji."""
    def handle_resize(self, width: int, height: int):
        self._validate_resize_params(width, height)

        new_width, new_height = self._calculate_new_dimensions(width, height)

        self.ui_manager.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    """Wczytywanie poziomów z pliku levels.json."""
    def load_levels(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(base_dir, ".."))
        levels_path = os.path.join(project_dir, "levels", "levels.json")

        try:
            with open(levels_path, "r") as level_file:
                self.levels = json.load(level_file)
        except FileNotFoundError:
            print(f"Ostrzeżenie: Nie znaleziono żadnych poziomów: {levels_path}")
            self.levels = {}
        except json.JSONDecodeError:
            print(f"BŁĄD: Nieprawidłowy json: {levels_path}")
            self.levels = {}

    """Oblicza nowe wymiary okna zachowując współczynnik proporcji."""
    @staticmethod
    def _calculate_new_dimensions(width: int, height: int) -> tuple[int, int]:
        new_width = width
        new_height = int(width / config.ASPECT_RATIO)

        if new_height > height:
            new_height = height
            new_width = int(new_height * config.ASPECT_RATIO)

        return new_width, new_height

    # Funkcje walidacyjne
    @staticmethod
    def _validate_delta_time(delta_time: float):
        if not isinstance(delta_time, float) or delta_time <= 0:
            raise ValueError("delta_time must be a positive float")

    @staticmethod
    def _validate_window_state(window_state: WindowState):
        if not isinstance(window_state, WindowState):
            raise ValueError("window_state must be an instance of WindowState")

    @staticmethod
    def _validate_resize_params(width: int, height: int):
        if not isinstance(width, int) or width <= 0:
            raise ValueError("width must be a positive integer")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("height must be a positive integer")