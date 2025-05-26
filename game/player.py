import pygame

from config import config
from game.floor import Floor

class Player:
    def __init__(self):
        self.x = config.PLAYER_START_X
        self.y = config.FLOOR_Y - config.PLAYER_OUTER_SIZE // 2
        self.outer_size = config.PLAYER_OUTER_SIZE
        self.inner_size = config.PLAYER_INNER_SIZE

        self.outer_color = config.PLAYER_OUTER_COLOR
        self.outer_rect = pygame.Rect(0, 0, self.outer_size, self.outer_size)
        self.outer_rect.center = (self.x, self.y)

        self.inner_color = config.PLAYER_INNER_COLOR
        self.inner_rect = pygame.Rect(0, 0, self.inner_size, self.inner_size)
        self.inner_rect.center = (self.x, self.y)

        self.speed = config.PLAYER_SPEED

        self.velocity_y = 0
        self.rotation = 0
        self.on_ground = False

        self.distance_to_floor = config.FLOOR_Y - self.y

        self.relative_air_position = 0.0

    def draw(self, screen: pygame.Surface, floor: Floor, camera_offset_x: int):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"
        assert isinstance(camera_offset_x, int), "camera_offset_x musi być liczbą całkowitą"

        self.update_size(screen, floor, camera_offset_x)

        pygame.draw.rect(screen, self.outer_color, self.outer_rect, border_radius=2)
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, border_radius=2)

    def update_size(self, screen: pygame.Surface, floor: Floor, camera_offset_x: int):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"
        assert isinstance(camera_offset_x, int), "camera_offset_x musi być liczbą całkowitą"

        screen_width, screen_height = screen.get_size()
        floor_y_screen = floor.get_screen_floor_y(screen)

        rect_outer_size = int(screen_width * (self.outer_size / config.SCREEN_WIDTH))
        rect_inner_size = int(screen_height * (self.inner_size / config.SCREEN_HEIGHT))

        world_x = self.x + camera_offset_x
        rect_x = int(screen_width * (world_x / config.SCREEN_WIDTH))

        ground_y_screen = floor_y_screen - rect_outer_size // 2

        if self.on_ground:
            rect_y = ground_y_screen
            self.relative_air_position = 0.0
        else:
            height_above_ground = ground_y_screen - self.y
            self.relative_air_position = height_above_ground / screen_height
            rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.outer_rect = pygame.Rect(0, 0, rect_outer_size, rect_outer_size)
        self.outer_rect.center = (rect_x, rect_y)

        self.inner_rect = pygame.Rect(0, 0, rect_inner_size, rect_inner_size)
        self.inner_rect.center = (rect_x, rect_y)