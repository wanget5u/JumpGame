import pygame.event

from pygame import VIDEORESIZE

from config import config
from config.enums import WindowState

from ui.ui_manager import UIManager

from game.player import Player
from game.engine import Engine
from game.floor import Floor

class GameManager:
    def __init__(self):
        self.running = False
        self.window_state = None

        self.floor = None
        self.player = None

        self.ui_manager = None
        self.engine = None

    def init(self):
        self.ui_manager = UIManager()
        self.ui_manager.init()

        self.floor = Floor(config.FLOOR_Y)
        self.engine = Engine(self.floor)

        self.player = Player()

        self.engine.reset_player(self.player)

        self.window_state = WindowState.MENU
        self.running = True

    def update(self, delta_time: float):
        assert isinstance(delta_time, float) and delta_time > 0, "delta_time musi być dodatnią liczbą zmiennoprzecinkową"

        if self.window_state == WindowState.GAME:
            self.engine.update_player(self.player, delta_time, self.ui_manager.window)
            self.handle_held_keys()

        self.poll_events()

    def handle_menu_events(self, event: pygame.event):
        self.ui_manager.start_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_quit()

    def handle_game_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.PAUSE)

    def handle_held_keys(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_UP] or mouse_buttons[0]:
            self.engine.player_jump(self.player)

    def handle_pause_events(self, event: pygame.event):
        self.ui_manager.resume_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))
        self.ui_manager.back_pause_button.handle_event(event, lambda: self.set_window_state(WindowState.MENU))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_window_state(WindowState.GAME)

    def is_running(self) -> bool:
        return self.running

    def game_quit(self):
        self.running = False

    def render(self):
        self.ui_manager.render(self.window_state, self.player, self.floor)

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