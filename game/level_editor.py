import json

import pygame, os

from game.floor import Floor
from ui.button import Button
from ui.label import Label
from ui.slider import Slider
from config import config

from objects.block import Block
from objects.spike import Spike
from objects.jump_pad import JumpPad
from objects.jump_orb import JumpOrb

class LevelEditor:
    def __init__(self, window: pygame.Surface, levels, floor: Floor):
        assert isinstance(window, pygame.Surface), "screen musi być instancją pygame.Surface"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"

        self.window = window
        self.levels = levels
        self.current_level_index = -1
        self.current_level = self.create_empty_level()

        self.floor = floor
        self.is_saved = False

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT

        # [EDITOR STATE]
        self.grid_size = config.GRID_SIZE
        self.camera_offset_x = 0

        self.selected_object = None
        self.selected_object_index = -1

        # select, delete, block, spike, jump_pad, jump_orb
        self.selected_tool = "select"
        self.selected_tool_label = None
        self.show_grid = True

        # [UI ELEMENTS]
        self.toolbar_height = config.TOOLBAR_HEIGHT
        self.name_input = ""
        self.difficulty_input = ""
        self.slider = None
        self.x_coordinate_label = None

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

        self.max_slider_x = config.MAX_SLIDER_X

        self.editor_view_init()

    def editor_view_init(self):
        self.select_button = Button(120, 770, 220, 70,"Select")
        self.delete_button = Button(120, 850, 220, 70,"Delete")

        self.block_button = Button(350, 770, 220, 70,"Block")
        self.spike_button = Button(350, 850, 220, 70,"Spike")

        self.jump_pad_button = Button(580, 770, 220, 70,"Jump Pad")
        self.jump_orb_button = Button(580, 850, 220, 70,"Jump Orb")

        self.save_button = Button(1480, 770, 220, 70,"Save")
        self.load_button = Button(1480, 850, 220, 70,"Load")
        self.exit_button = Button(1250, 850, 220, 70,"Exit")

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

        self.selected_tool_label = Label(
            920, 850, "")

        self.change_tool("select")

        self.slider = Slider(
            self.screen_width // 2, 60,
            500, 80, 0, self.max_slider_x,0)

        self.x_coordinate_label = Label(
            self.screen_width // 2, 125, "")

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

    def load_level(self, index: int):
        assert isinstance(index, int) and index > 0, "index musi być dodatnią liczbą całkowitą"

        for level in self.levels:
            if int(level["index"]) == index:
                self.current_level = level.copy()
                self.current_level_index = index
                self.name_input = level["name"]
                self.difficulty_input = level["difficulty"]

    def create_empty_level(self) -> list:
        self.current_level_index = len(self.levels)
        return \
            {
            "index": str(len(self.levels) + 1),
            "name": "New Level",
            "difficulty": "easy",
            "layout": []
            }

    def change_tool(self, tool_name: str):
        assert isinstance(tool_name, str), "tool_name musi być stringiem"
        self.selected_tool = tool_name
        self.selected_tool_label.set_text("Current tool: " + tool_name[0].upper() + tool_name[1::].replace("_", " "))

    def select_object_at_position(self, position: tuple):
        assert isinstance(position, tuple) and all(isinstance(x, int) for x in position), "position musi być krotką 2 liczb całkowitych"

        self.selected_object = None
        self.selected_object_index = -1

        for x in range(len(self.current_level["layout"]) - 1, -1, -1):
            obj = self.current_level["layout"][x]
            if self.is_point_in_object(position, obj):
                self.selected_object = obj
                self.selected_object_index = x
                break

    def is_point_in_object(self, position, obj):
        assert isinstance(position, tuple) and all(isinstance(x, int) for x in position), "position musi być krotką 2 liczb całkowitych"

        x, y = position

        if obj["type"] == "block":
            temp_block = Block(obj["x"], obj["y"])
            temp_block.update_size(self.window)
            return temp_block.outer_rect.collidepoint(self.world_to_screen((x, y)))
        elif obj["type"] == "spike":
            radius = 20
            dx = x - obj["x"]
            dy = y - obj["y"]
            return (dx * dx + dy * dy) <= radius * radius
        elif obj["type"] in ["jump_pad", "jump_orb"]:
            radius = 20
            dx = x - obj["x"]
            dy = y - obj["y"]
            return (dx * dx + dy * dy) <= radius * radius

        return False

    def screen_to_world(self, screen_pos):
        assert isinstance(screen_pos, tuple) and all(isinstance(x, int) for x in screen_pos), "screen_pos musi być krotką 2 liczb całkowitych"
        x, y = screen_pos
        return x - self.camera_offset_x, y

    def world_to_screen(self, world_pos: tuple):
        assert isinstance(world_pos, tuple) and all(isinstance(x, int) for x in world_pos), "world_pos musi być krotką 2 liczb całkowitych"
        x, y = world_pos
        return x + self.camera_offset_x, y

    def draw_grid(self):
        screen_width, screen_height = self.window.get_size()

        width_scale = screen_width / self.screen_width
        height_scale = screen_height / self.screen_height

        self.grid_size = int(config.GRID_SIZE * min(width_scale, height_scale))
        self.toolbar_height = int(config.TOOLBAR_HEIGHT * height_scale)

        start_x = (self.camera_offset_x % self.grid_size)
        start_y = 0

        grid_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        x = start_x
        while x < screen_width:
            pygame.draw.line(grid_surface, self.grid_color, (x, 0), (x, screen_height - self.toolbar_height))
            x += self.grid_size

        y = start_y
        while y < screen_height - self.toolbar_height:
            pygame.draw.line(grid_surface, self.grid_color, (0, y), (screen_width, y))
            y += self.grid_size

        start_world_x = self.grid_size * 2
        screen_x = start_world_x + self.camera_offset_x

        if 0 <= screen_x < screen_width:
            pygame.draw.line(
                grid_surface,
                config.GRID_START_LINE_COLOR,
                (screen_x, 0),
                (screen_x, screen_height - self.toolbar_height), 2)

        self.window.blit(grid_surface, (0, 0))

    def update_slider_x(self):
        furthest_obj_x = 0

        for obj in self.current_level["layout"]:
            if obj["x"] > furthest_obj_x:
                furthest_obj_x = obj["x"]

        if furthest_obj_x + config.SLIDER_MARGIN > self.slider.max_val:
            self.slider.max_val = furthest_obj_x + config.SLIDER_MARGIN

    def draw_objects(self):
        for x, obj in enumerate(self.current_level["layout"]):
            is_selected = (x == self.selected_object_index)
            self.draw_object(obj, is_selected)

    def draw_object(self, obj, is_selected):
        assert isinstance(is_selected, bool), "is_selected musi być wartością boolowską"

        obj_type = obj["type"]
        screen_pos = self.world_to_screen((obj["x"], obj["y"]))

        if is_selected:
            highlight_color = config.HIGHLIGHT_COLOR

            if obj_type == "block":
                rect = pygame.Rect(
                    screen_pos[0] - self.grid_size // 2 - 2,
                    screen_pos[1] - self.grid_size // 2 - 2,
                    self.grid_size + 4,
                    self.grid_size + 4
                )
                pygame.draw.rect(self.window, highlight_color, rect, 2)
            else:
                pygame.draw.circle(self.window, highlight_color, (screen_pos[0], screen_pos[1]), self.grid_size // 2, 2)

        types = {
            "block" : Block(screen_pos[0], screen_pos[1]),
            "spike" : Spike(screen_pos[0], screen_pos[1]),
            "jump_orb" : JumpOrb(screen_pos[0], screen_pos[1]),
            "jump_pad": JumpPad(screen_pos[0], screen_pos[1])
        }

        types[obj_type].draw(self.window)


    def add_object(self, obj_type: str, position):
        assert isinstance(position, tuple) and all(isinstance(x, int) for x in position), "position musi być krotką 2 liczb całkowitych"

        world_pos = self.screen_to_world(pygame.mouse.get_pos())

        if world_pos[1] > self.floor.floor_y:
            return

        x = ((world_pos[0] // self.grid_size) * self.grid_size) + self.grid_size // 2
        y = ((world_pos[1] // self.grid_size) * self.grid_size) + self.grid_size // 2

        new_obj = {"type": obj_type, "x": x, "y": y}

        self.current_level["layout"].append(new_obj)
        self.selected_object = new_obj
        self.selected_object_index = len(self.current_level["layout"]) - 1

        self.update_slider_x()

    def delete_object(self):
        world_pos = self.screen_to_world(pygame.mouse.get_pos())

        if world_pos[1] > self.floor.floor_y:
            return

        grid_x = world_pos[0] // self.grid_size
        grid_y = world_pos[1] // self.grid_size

        for index, obj in enumerate(self.current_level["layout"]):
            obj_x = obj["x"]
            obj_y = obj["y"]

            obj_grid_x = obj_x // self.grid_size
            obj_grid_y = obj_y // self.grid_size

            if obj_grid_x == grid_x and obj_grid_y == grid_y:
                del self.current_level["layout"][index]
                self.selected_object = None
                self.selected_object_index = -1
                break

    def handle_event(self, event: pygame.event, save_button_event, load_button_event, exit_button_event):
        self.select_button.handle_event(event, lambda: self.change_tool("select"))
        self.delete_button.handle_event(event, lambda: self.change_tool("delete"))
        self.block_button.handle_event(event, lambda: self.change_tool("block"))
        self.spike_button.handle_event(event, lambda: self.change_tool("spike"))
        self.jump_pad_button.handle_event(event, lambda: self.change_tool("jump_pad"))
        self.jump_orb_button.handle_event(event, lambda: self.change_tool("jump_orb"))

        self.save_button.handle_event(event, save_button_event)
        self.load_button.handle_event(event, load_button_event)
        self.exit_button.handle_event(event, exit_button_event)

        self.slider.handle_event(event)
        self.camera_offset_x = -round(self.slider.value)
        self.x_coordinate_label.set_text(str(round(self.slider.value)))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            world_pos = self.screen_to_world(mouse_pos)

            if self.slider.outer_rect.collidepoint(mouse_pos):
                return

            match self.selected_tool:
                case "select":
                    self.select_object_at_position(world_pos)
                case "delete":
                    self.delete_object()
                case "block":
                    self.add_object(self.selected_tool, world_pos)
                case "spike":
                    self.add_object(self.selected_tool, world_pos)
                case "jump_pad":
                    self.add_object(self.selected_tool, world_pos)
                case "jump_orb":
                    self.add_object(self.selected_tool, world_pos)

    def render(self):
        self.draw_grid()
        self.draw_objects()

        self.floor.draw(self.window)
        self.selected_tool_label.draw(self.window)

        self.slider.draw(self.window)
        self.x_coordinate_label.draw(self.window)

        for name, button in self.buttons.items():
            button.draw(self.window)