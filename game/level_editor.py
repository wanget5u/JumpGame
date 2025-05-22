import json

import pygame, os

from game.floor import Floor
from ui.button import Button
from config import config

class LevelEditor:
    def __init__(self, window: pygame.Surface, levels: list, floor: Floor):
        assert isinstance(window, pygame.Surface), "screen musi być instancją pygame.Surface"
        assert isinstance(levels, list), "list musi być listą"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"

        self.window = window
        self.levels = levels
        self.current_level_index = len(levels)
        self.current_level = self.create_empty_level()

        self.floor = floor

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

        # [EDITOR STATE]
        self.grid_size = config.GRID_SIZE
        self.camera_offset_x = 0
        self.camera_offset_y = 0

        self.selected_object = None
        self.selected_object_index = -1

        # select, delete, block, spike, jump_pad, jump_orb
        self.selected_tool = "select"
        self.show_grid = True

        # [UI ELEMENTS]
        self.toolbar_height = config.TOOLBAR_HEIGHT
        self.name_input = ""
        self.difficulty_input = ""

        # [UI COLORS]
        self.toolbar_color = config.TOOLBAR_COLOR
        self.text_color = config.TEXT_COLOR
        self.grid_color = config.GRID_COLOR

        # [BUTTONS]
        self.select_button = None
        self.delete_button = None
        self.block_button = None
        self.spike_button = None
        self.jump_pad_button = None
        self.jump_orb_button = None

        self.save_button = None
        self.load_button = None
        self.exit_button = None

        self.buttons = {}

        self.editor_view_init()

    def editor_view_init(self):
        self.select_button = Button(130, 740, 220, 80,"Select")
        self.delete_button = Button(130, 840, 220, 80,"Delete")

        self.block_button = Button(370, 740, 220, 80,"Block")
        self.spike_button = Button(370, 840, 220, 80,"Spike")

        self.jump_pad_button = Button(610, 740, 220, 80,"Jump Pad")
        self.jump_orb_button = Button(610, 840, 220, 80,"Jump Orb")

        self.save_button = Button(1470, 740, 220, 80,"Save")
        self.load_button = Button(1470, 840, 220, 80,"Load")
        self.exit_button = Button(1230, 840, 220, 80,"Exit")

        self.buttons = \
            {
                "select" : self.select_button,
                "delete" : self.delete_button,
                "block" : self.block_button,
                "spike" : self.spike_button,
                "jump_pad" : self.jump_pad_button,
                "jump_orb" : self.jump_orb_button,
                "save" : self.save_button,
                "load" : self.load_button,
                "exit" : self.exit_button
            }

    def save_levels(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
        levels_path = os.path.join(PROJECT_DIR, "levels", "levels.json")

        if int(self.current_level["index"]) > len(self.levels):
            self.levels.append(self.current_level)
        else:
            for index, level in enumerate(self.levels):
                if level["index"] == self.current_level["index"]:
                    self.levels[index] = self.current_level
                    break

        with open(levels_path, "w") as file:
            json.dump(self.levels, file, indent=2)

        print(f"Zapisano {len(self.levels)} poziom do {levels_path}.")

    def load_level(self, index: int):
        assert isinstance(index, int) and index > 0, "index musi być dodatnią liczbą całkowitą"

        for level in self.levels:
            if int(level["index"]) == index:
                self.current_level = level.copy()
                self.current_level_index = index
                self.name_input = level["name"]
                self.difficulty_input = level["difficulty"]

        print(f"Wczytano poziom {self.name_input}.")

    def create_empty_level(self) -> list:
        pass

    def handle_event(self, event: pygame.event):
        pass

    def render(self):
        for name, button in self.buttons.items():
            button.draw(self.window)