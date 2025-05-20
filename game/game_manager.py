import pygame.event

from config.enums import WindowState
from ui.ui_manager import UIManager

class GameManager:
    def __init__(self):
        self.running = False
        self.window_state = None

        self.ui_manager = UIManager()
        self.window_state = WindowState.MENU
        self.running = True

    def is_running(self) -> bool:
        return self.running

    def game_quit(self):
        self.running = False

    def update(self):
        self.poll_events()

    def poll_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.game_quit()

            if self.window_state == WindowState.MENU:
                self.ui_manager.start_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_quit()

            if self.window_state == WindowState.GAME:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.set_window_state(WindowState.MENU)

    def render(self):
        self.ui_manager.render(self.window_state)

    def set_window_state(self, window_state: WindowState):
        assert isinstance(window_state, WindowState), "window_state musi być instancją WindowState"
        self.window_state = window_state