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

        self.objects = []
        self.camera_offset_x = 0

    def _check_player_coherence(self, player: Player) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        return player.outer_rect.bottom <= self.floor.floor_y

    """ Sprawdza kolizję gracza z przeszkodą """
    def check_player_collision_with_object(self, player: Player, obstacle_rect: pygame.Rect) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(obstacle_rect, pygame.Rect), "obstacle_rect musi być instancją pygame.Rect"
        return player.outer_rect.colliderect(obstacle_rect)

    def check_player_collision_with_objects(self, player: Player, screen: pygame.Surface):
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        deadly_collision = False
        collision_detected = False
        interactive_collisions = []

        for obj in self.objects:
            obj.update_size(screen)

            if hasattr(obj, 'get_collision_rect'):
                collision_rect = obj.get_collision_rect()
                collision_detected = player.outer_rect.colliderect(collision_rect)

                if collision_detected and obj.__class__.__name__ == 'Spike':
                    if hasattr(obj, 'get_collision_points'):
                        collision_detected = self.point_in_polygon_collision(player.outer_rect, obj.get_collision_points())

            if collision_detected:
                obj_type = obj.__class__.__name__

                if obj_type in ['Block', 'Spike']:
                    deadly_collision = True
                elif obj_type in ['JumpPad', 'JumpOrb']:
                    interactive_collisions.append(obj)

        for obj in interactive_collisions:
            self.player_jump(player)

        return deadly_collision

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

    def point_in_polygon(self, point: tuple, polygon_points: list):
        assert isinstance(point, tuple) and all(isinstance(x, int) for x in point), "point musi być krotką 2 dodatnich liczb całkowitych"
        assert isinstance(polygon_points, list), "polygon_points musi być listą"

        point = Point(point)
        polygon = Polygon(polygon_points)
        return polygon.contains(point)

    """ Aktualizuje pozycję gracza na podstawie prędkości, grawitacji i czasu (delta_time):
    Dodaje grawitację, przesuwa gracza, obsługuje wykrycie kolizji z podłożem (floor_y) """
    def update_player(self, player: Player, delta_time: float, screen: pygame.Surface):
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(delta_time, float) and delta_time > 0, "delta_time musi być dodatnią liczbą zmiennoprzecinkową"
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        self.apply_gravity(player, delta_time)

        player.y += player.velocity_y * delta_time

        floor_y_screen = self.floor.get_screen_floor_y(screen)

        ground_y = floor_y_screen - player.outer_rect.height / 2

        player.update_size(screen, self.floor)

        self.camera_offset_x -= config.PLAYER_SPEED

        if self.check_player_collision_with_floor(player, screen):
            player.y = ground_y
            player.velocity_y = 0
            player.on_ground = True
        else:
            player.on_ground = False

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

        player.x = 100
        player.y = self.floor.floor_y
        player.velocity_y = 0
        player.rotation = 0
        player.on_ground = True

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
            obj_type = obj.__class__.__name__
            screen_pos = self.world_to_screen((obj.x, obj.y))

            if obj_type == 'Block':
                block = Block(screen_pos[0], screen_pos[1])
                block.draw(screen)
            elif obj_type == 'Spike':
                spike = Spike(
                    screen_pos[0] + config.GRID_SIZE // 2,
                    screen_pos[1] + config.GRID_SIZE)
                spike.draw(screen)

    def world_to_screen(self, world_pos: tuple):
        assert isinstance(world_pos, tuple) and all(isinstance(x, int) for x in world_pos), "world_pos musi być krotką 2 liczb całkowitych"
        x, y = world_pos
        return x + self.camera_offset_x, y