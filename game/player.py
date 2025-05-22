import pygame

from config import config

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

    def draw(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.update_size(screen)

        pygame.draw.rect(screen, self.outer_color, self.outer_rect, border_radius=2)
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, border_radius=2)

    def update_size(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        screen_width, screen_height = screen.get_size()

        rect_outer_size = int(screen_width * (self.outer_size / config.SCREEN_WIDTH))
        rect_inner_size = int(screen_height * (self.inner_size / config.SCREEN_HEIGHT))
        rect_x = int(screen_width * (self.x / config.SCREEN_WIDTH))
        rect_y = int(screen_height * (self.y / config.SCREEN_HEIGHT))

        self.outer_rect = pygame.Rect(0, 0, rect_outer_size, rect_outer_size)
        self.outer_rect.center = (rect_x, rect_y)

        self.inner_rect = pygame.Rect(0, 0, rect_inner_size, rect_inner_size)
        self.inner_rect.center = (rect_x, rect_y)

