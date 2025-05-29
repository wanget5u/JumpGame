import pygame

from config import config
from game.player import Player
from game.floor import Floor

from objects.block import Block
from objects.spike import Spike
from objects.jump_pad import JumpPad
from objects.jump_orb import JumpOrb

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class Engine:
    def __init__(self, floor: Floor):
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"

        self.floor = floor
        self.gravity = 4500
        self.jump_force = -1350

        self.original_screen_height = config.SCREEN_HEIGHT
        self.original_screen_width = config.SCREEN_WIDTH

        self.attempts = 1

        self.objects = []
        self.camera_offset_x = 0

    """ Sprawdza kolizję gracza z przeszkodą """
    @staticmethod
    def check_player_collision_with_object(player: Player, obstacle_rect: pygame.Rect) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(obstacle_rect, pygame.Rect), "obstacle_rect musi być instancją pygame.Rect"
        return player.outer_rect.colliderect(obstacle_rect)

    def point_in_polygon_collision(self, outer_rect: pygame.Rect, polygon_points: list):
        assert isinstance(outer_rect, pygame.Rect), "outer_rect musi być obiektem pygame.Rect"
        assert isinstance(polygon_points, list), "polygon_points musi być listą"

        rect_points = [
            (outer_rect.left, outer_rect.top),
            (outer_rect.right, outer_rect.top),
            (outer_rect.left, outer_rect.bottom),
            (outer_rect.right, outer_rect.bottom)
        ]

        for point in rect_points:
            if self.point_in_polygon(point, polygon_points):
                return True

        for point in polygon_points:
            if outer_rect.collidepoint(point):
                return True

        return False

    @staticmethod
    def point_in_polygon(point: tuple, polygon_points: list):
        assert isinstance(point, tuple) and all(isinstance(x, int) for x in point), "point musi być krotką 2 dodatnich liczb całkowitych"
        assert isinstance(polygon_points, list), "polygon_points musi być listą"

        point = Point(point)
        polygon = Polygon(polygon_points)
        return polygon.contains(point)

    def check_block_collision_top(self, player: Player, new_y: float):
        player_bottom = new_y + config.PLAYER_OUTER_SIZE // 2
        player_left = player.x - config.PLAYER_OUTER_SIZE // 2
        player_right = player.x + config.PLAYER_OUTER_SIZE // 2

        highest_block_top = None

        for obj in self.objects:
            if obj.__class__.__name__ == 'Block':
                block_size = config.BLOCK_OUTER_SIZE
                block_left = obj.x - block_size // 2
                block_right = obj.x + block_size // 2
                block_top = obj.y - block_size // 2
                block_bottom = obj.y + block_size // 2

                if player_right >= block_left and player_left <= block_right:
                    if player.velocity_y >= 0 and block_top <= player_bottom <= block_bottom:
                        if highest_block_top is None or block_top < highest_block_top:
                            highest_block_top = block_top

        return highest_block_top

    def check_block_collision_left_bottom(self, player: Player, new_x: float):
        player_left = new_x - config.PLAYER_OUTER_SIZE // 2
        player_right = new_x + config.PLAYER_OUTER_SIZE // 2
        player_top = player.y - config.PLAYER_OUTER_SIZE // 2
        player_bottom = player.y + config.PLAYER_OUTER_SIZE // 2

        for obj in self.objects:
            if obj.__class__.__name__ == 'Block':
                block_left = obj.x - config.BLOCK_OUTER_SIZE // 2
                block_right = obj.x + config.BLOCK_OUTER_SIZE // 2
                block_top = obj.y - config.BLOCK_OUTER_SIZE // 2
                block_bottom = obj.y + config.BLOCK_OUTER_SIZE // 2

                if player_right > block_left and player_left < block_right and player_bottom > block_top and player_top < block_bottom:
                    return True

        return False

    """ Aktualizuje pozycję gracza na podstawie prędkości, grawitacji i czasu (delta_time):
    Dodaje grawitację, przesuwa gracza, obsługuje wykrycie kolizji z podłożem (floor_y) """
    def update_player(self, player: Player, delta_time: float, screen: pygame.Surface):
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(delta_time, float) and delta_time > 0, "delta_time musi być dodatnią liczbą zmiennoprzecinkową"
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.apply_gravity(player, delta_time)

        new_y = player.y + player.velocity_y * delta_time

        block_top = self.check_block_collision_top(player, new_y)

        floor_y = self.floor.floor_y
        ground_y = floor_y - config.PLAYER_OUTER_SIZE // 2

        player_bottom = new_y + config.PLAYER_OUTER_SIZE // 2

        next_y = new_y
        on_ground = False

        landing_y = ground_y
        if block_top is not None and player.velocity_y >= 0:
            block_landing_y = block_top - config.PLAYER_OUTER_SIZE // 2
            if player_bottom >= block_top:
                next_y = block_landing_y
                player.velocity_y = 0
                on_ground = True

        elif player_bottom >= floor_y:
            next_y = floor_y - config.PLAYER_OUTER_SIZE // 2
            player.velocity_y = 0
            on_ground = True

        player.y = next_y
        player.on_ground = on_ground

        new_x = player.x + config.PLAYER_SPEED * delta_time
        if not self.check_block_collision_left_bottom(player, new_x):
            player.x = new_x
        else:
            return True

        if player.x >= config.SCREEN_WIDTH // 6:
            target_camera_x = -(player.x - config.SCREEN_WIDTH // 6)
            self.camera_offset_x = int(target_camera_x)

    """ Powoduje skok gracza: nadaje prędkość w górę, sprawdza, czy gracz jest na ziemi, zanim pozwoli na skok """
    def player_jump(self, player: Player):
        assert isinstance(player, Player), "player musi być instancją klasy Player"

        if player.on_ground:
            screen_height = pygame.display.get_surface().get_height()
            scaled_jump_force = self.jump_force * (screen_height / self.original_screen_height)

            player.velocity_y = scaled_jump_force
            player.on_ground = False
            player.rotation = (player.rotation + 180) % 360

    """ Zwraca True, jeżeli gracz dotknął podłoża """
    def check_player_collision_with_floor(self, player: Player, screen: pygame.Surface) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        return player.outer_rect.bottom >= self.floor.get_screen_floor_y(screen)

    """ Zwraca True, jeśli gracz zderzył się z przeszkodą lub spadł poza ekran """
    def is_game_over(self, player: Player, obstacles: list[pygame.Rect]) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(obstacles, list) and all(isinstance(rect, pygame.Rect) for rect in obstacles), "rect musi być instancją pygame.Rect"

        if player.y > config.SCREEN_HEIGHT:
            return True

        for obstacle in obstacles:
            if self.check_player_collision_with_object(player, obstacle):
                return True

        return False

    def reset_player(self, player: Player):
        assert isinstance(player, Player), "player musi być instancją klasy Player"

        player.x = 90
        player.y = self.floor.floor_y - 10
        player.velocity_y = 0
        player.rotation = 0
        player.on_ground = True
        self.camera_offset_x = 0

    def apply_gravity(self, player: Player, delta_time: float):
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(delta_time, float) and delta_time > 0, "delta_time musi być dodatnią liczbą zmiennoprzecinkową"
        screen_height = pygame.display.get_surface().get_height()
        scaled_gravity = self.gravity * (screen_height / self.original_screen_height)

        player.velocity_y += scaled_gravity * delta_time

    def set_objects_from_layout(self, layout: list):
        assert isinstance(layout, list), "layout musi być listą"

        type_map = \
        {
            "block": Block,
            "spike": Spike,
            "jump_pad": JumpPad,
            "jump_orb": JumpOrb
        }

        self.objects = [type_map[obj["type"]](obj["x"], obj["y"]) for obj in layout if obj["type"] in type_map]

    def draw_objects(self, screen: pygame.Surface):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        for obj in self.objects:
            screen_x = obj.x + self.camera_offset_x
            screen_y = obj.y

            if -100 < screen_x < config.SCREEN_WIDTH + 100:
                obj_type = obj.__class__.__name__

                if obj_type == 'Block':
                    temp_block = Block(screen_x, screen_y)
                    temp_block.update_size(screen)
                    temp_block.draw(screen)

                elif obj_type == 'Spike':
                    temp_spike = Spike(screen_x, screen_y)
                    temp_spike.update_size(screen)
                    temp_spike.draw(screen)

    def world_to_screen(self, world_pos: tuple):
        assert isinstance(world_pos, tuple) and all(isinstance(x, int) for x in world_pos), "world_pos musi być krotką 2 liczb całkowitych"
        x, y = world_pos
        return x + self.camera_offset_x, y

    def get_furthest_object_x(self):
        furthest_x = 0

        for obj in self.objects:
            if obj.x > furthest_x:
                furthest_x = obj.x

        if furthest_x == 0:
            furthest_x = config.MIN_LEVEL_LENGTH

        return furthest_x + config.END_WALL_X