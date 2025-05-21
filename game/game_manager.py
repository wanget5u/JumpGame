import pygame.event
from pygame import VIDEORESIZE

from config import config
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

            if event.type == VIDEORESIZE:
                width, height = event.w, event.h
                self.handle_resize(width, height)

            if event.type == pygame.QUIT:
                self.game_quit()

            if self.window_state == WindowState.MENU:
                self.ui_manager.start_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_quit()

            elif self.window_state == WindowState.GAME:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.set_window_state(WindowState.PAUSE)

            elif self.window_state == WindowState.PAUSE:
                self.ui_manager.resume_button.handle_event(event, lambda: self.set_window_state(WindowState.GAME))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.set_window_state(WindowState.GAME)

    def render(self):
        self.ui_manager.render(self.window_state)

    def set_window_state(self, window_state: WindowState):
        assert isinstance(window_state, WindowState), "window_state musi być instancją WindowState"

        print(f"[DEBUG] Zmieniam stan: {self.window_state} -> {window_state}")
        self.window_state = window_state

    def handle_resize(self, width: int, height: int):
        assert isinstance(width, int) and width > 0 and isinstance(height, int) and height > 0, "width i height muszą być dodatnimi liczbami całkowitymi"

        new_width = width
        new_height = int(width / config.ASPECT_RATIO)

        if new_height > height:
            new_height = height
            new_width = int(new_height * config.ASPECT_RATIO)

        self.ui_manager.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)