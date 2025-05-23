import json, os

import pygame.event

from pygame import VIDEORESIZE

from config import config
from config.enums import WindowState

from ui.ui_manager import UIManager

from game.level_editor import LevelEditor
from game.player import Player
from game.engine import Engine
from game.floor import Floor

class GameManager:
    def __init__(self):
        self.running = False
        self.window_state = None

        self.floor = None
        self.player = None
        self.levels = {}

        # [MANAGERS]
        self.ui_manager = None
        self.engine = None
        self.level_editor = None

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

    def update(self, delta_time: float):
        assert isinstance(delta_time, float) and delta_time > 0, "delta_time musi być dodatnią liczbą zmiennoprzecinkową"

        if self.window_state == WindowState.GAME:
            self.engine.update_player(self.player, delta_time, self.ui_manager.window)

        self.poll_events()

    def handle_menu_events(self, event: pygame.event):
        self.ui_manager.start_button.handle_event(event, lambda: self.set_window_state(WindowState.SELECT))
        self.ui_manager.level_editor_button.handle_event(event, lambda: self.set_window_state(WindowState.EDIT))
        self.ui_manager.exit_button.handle_event(event, lambda: self.game_quit())

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_quit()

    def handle_game_events(self, event: pygame.event):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_UP] or mouse_buttons[0]:
            self.engine.player_jump(self.player)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.PAUSE)

    def handle_pause_events(self, event: pygame.event):
        self.ui_manager.resume_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))
        self.ui_manager.back_pause_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.GAME)

    def handle_level_select_events(self, event: pygame.event):
        self.ui_manager.level_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.ui_manager.change_level_select_page("left")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.ui_manager.change_level_select_page("right")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.MENU)

    def handle_level_editor_events(self, event: pygame.event):
        def exit_button_event():
            if self.level_editor.is_saved:
                self.set_window_state(WindowState.MENU)
            else:
                self.set_window_state(WindowState.EDIT_CONFIRM)

        self.level_editor.handle_event(event, exit_button_event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.EDIT_CONFIRM)

    def handle_edit_confirm_events(self, event):
        self.ui_manager.edit_confirm_yes_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))
        self.ui_manager.edit_confirm_no_button.handle_event(event, lambda: self.set_window_state(WindowState.EDIT))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.EDIT)

    def is_running(self) -> bool:
        return self.running

    def game_quit(self):
        self.running = False

    def render(self):
        self.ui_manager.render(self.window_state, self.player, self.floor, self.level_editor)

    def set_window_state(self, window_state: WindowState):
        assert isinstance(window_state, WindowState), "window_state musi być instancją WindowState"

        self.window_state = window_state

    def handle_resize(self, width: int, height: int):
        assert isinstance(width, int) and width > 0 and isinstance(height, int) and height > 0, "width i height muszą być dodatnimi liczbami całkowitymi"

        new_width = width
        new_height = int(width / config.ASPECT_RATIO)

        if new_height > height:
            new_height = height
            new_width = int(new_height * config.ASPECT_RATIO)

        self.ui_manager.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

        if self.player and self.floor:
            if self.player.on_ground:
                floor_y = self.floor.get_screen_floor_y(self.ui_manager.window)
                self.player.y = floor_y - self.player.outer_rect.height / 2

    def load_levels(self):
        BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

        levels_path = os.path.join(PROJECT_DIR, "levels", "levels.json")

        with open(levels_path, "r") as level:
            self.levels = json.load(level)

    def poll_events(self):
        for event in pygame.event.get():

            if event.type == VIDEORESIZE:
                self.handle_resize(event.w, event.h)

            if event.type == pygame.QUIT:
                self.game_quit()

            if self.window_state == WindowState.MENU:
                self.handle_menu_events(event)

            elif self.window_state == WindowState.GAME:
                self.handle_game_events(event)

            elif self.window_state == WindowState.PAUSE:
                self.handle_pause_events(event)

            elif self.window_state == WindowState.SELECT:
                self.handle_level_select_events(event)

            elif self.window_state == WindowState.EDIT:
                self.handle_level_editor_events(event)

            elif self.window_state == WindowState.EDIT_CONFIRM:
                self.handle_edit_confirm_events(event)