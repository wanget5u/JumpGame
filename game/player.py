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
        self.on_ground = False

        self.distance_to_floor = config.FLOOR_Y - self.y

    def draw(self, screen: pygame.Surface, camera_offset_x: int):
        self._validate_draw_params(screen, camera_offset_x)

        self._update_size(screen, camera_offset_x)

        pygame.draw.rect(screen, self.outer_color, self.outer_rect, border_radius=2)
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, border_radius=2)

    def _update_size(self, screen: pygame.Surface, camera_offset_x: int):

        screen_width, screen_height = screen.get_size()

        rect_outer_size = int(screen_width * (self.outer_size / config.SCREEN_WIDTH))
        rect_inner_size = int(screen_height * (self.inner_size / config.SCREEN_HEIGHT))

        world_x = self.x + camera_offset_x
        rect_x = int(screen_width * (world_x / config.SCREEN_WIDTH))
        rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.outer_rect = pygame.Rect(0, 0, rect_outer_size, rect_outer_size)
        self.outer_rect.center = (rect_x, rect_y)

        self.inner_rect = pygame.Rect(0, 0, rect_inner_size, rect_inner_size)
        self.inner_rect.center = (rect_x, rect_y)

    @staticmethod
    def _validate_draw_params(screen: pygame.Surface, camera_offset_x: int):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")
        if not isinstance(camera_offset_x, int):
            raise ValueError("camera_offset_x musi być liczbą całkowitą")