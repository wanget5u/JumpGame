import pygame

from typing import List, Optional, Tuple, Union

from config import config
from game.end_wall import EndWall
from game.player import Player
from game.floor import Floor

from objects.block import Block
from objects.spike import Spike
from objects.jump_pad import JumpPad
from objects.jump_orb import JumpOrb

"""Główny silnik gry odpowiedzialny za fizykę, kolizje i zarządzanie obiektami."""
class Engine:
    def __init__(self, floor: Floor):
        self._validate_floor(floor)

        self.floor = floor
        self.gravity = 4500
        self.jump_force = -1350

        # Oryginalne wymiary ekranu do skalowania
        self.original_screen_height = config.SCREEN_HEIGHT
        self.original_screen_width = config.SCREEN_WIDTH

        self.attempts = 1  # Liczba prób
        self.objects: List[Union[Block, Spike, JumpPad, JumpOrb]] = []
        self.camera_offset_x = 0

        self.end_wall: Optional[EndWall] = None
        self.on_orb = False

    """Aktualizuje pozycję gracza na podstawie prędkości, grawitacji i czasu."""
    def update_player(self, player: Player, delta_time: float, screen: pygame.Surface) -> bool:
        """ Args:
                 player: Gracz do aktualizacji
                 delta_time: Czas od ostatniej klatki
                 screen: Powierzchnia ekranu
             Returns:
                 True, jeśli gra się skończyła (kolizja); False w przeciwnym razie
        """
        self._validate_update_params(player, delta_time, screen)

        self._apply_gravity(player, delta_time)

        # Aktualizuj pozycję Y gracza
        game_over = self._update_vertical_movement(player, delta_time)
        if game_over: return True

        # Aktualizuj pozycję X gracza
        game_over = self._update_horizontal_movement(player, delta_time)
        if game_over: return True

        for obj in self.objects:
            if not (isinstance(obj, JumpOrb) or isinstance(obj, JumpPad)):
                continue

            player_bounds = self._get_block_bounds(player)
            object_bounds = self._get_block_bounds(obj)

            if isinstance(obj, JumpPad):
                if self._rectangles_overlap(object_bounds, player_bounds):
                    self.player_jump(player, 1.3)

            elif isinstance(obj, JumpOrb):
                if self._rectangles_overlap(object_bounds, player_bounds):
                    keys = pygame.key.get_pressed()
                    mouse_buttons = pygame.mouse.get_pressed()

                    if keys[pygame.K_UP] or mouse_buttons[0]: self.player_jump(player, 0.9, True)

        self._update_camera(player)

        return False

    """Aktualizuje ruch pionowy gracza i sprawdza kolizje z blokami i podłożem."""
    def _update_vertical_movement(self, player: Player, delta_time: float) -> bool:
        """ Args:
                 player: Gracz do aktualizacji
                 delta_time: Czas od ostatniej klatki
             Returns:
                 True, jeśli wystąpiła kolizja; False, jeśli ta kolizja nie wystąpiła
        """
        new_y = player.y + player.velocity_y * delta_time

        block_top = self._check_block_collision_top(player, new_y)
        floor_y = self.floor.floor_y
        player_bottom = new_y + config.PLAYER_OUTER_SIZE // 2

        if block_top is not None and player.velocity_y >= 0 and player_bottom >= block_top:
            player.y = block_top - config.PLAYER_OUTER_SIZE // 2
            player.velocity_y = 0
            player.on_ground = True
        elif player_bottom >= floor_y:
            player.y = floor_y - config.PLAYER_OUTER_SIZE // 2
            player.velocity_y = 0
            player.on_ground = True
        else:
            player.y = new_y
            player.on_ground = False

        return False

    """Aktualizuje ruch poziomy gracza i sprawdza kolizje z blokami."""
    def _update_horizontal_movement(self, player: Player, delta_time: float) -> bool:
        """ Args:
                 player: Gracz do aktualizacji
                 delta_time: Czas od ostatniej klatki
             Returns:
                 True, jeśli wystąpiła kolizja; False, jeśli ta kolizja nie wystąpiła
        """
        new_x = player.x + config.PLAYER_SPEED * delta_time

        if not self._check_block_collision_horizontal(player, new_x):
            player.x = new_x
            return False
        else:
            return True

    """Aktualizuje pozycję kamery na podstawie pozycji gracza."""
    def _update_camera(self, player: Player):
        """ Args:
                player: Gracz, za którym podąża kamera
        """
        if player.x >= config.SCREEN_WIDTH // 6:
            target_camera_x = -(player.x - config.SCREEN_WIDTH // 6)
            self.camera_offset_x = int(target_camera_x)

    """Wykonuje skok gracza jeśli jest na ziemi."""

    def player_jump(self, player: Player, multiply: [int, float] = 1, force_jump: bool = False):
        """ Args:
                player: Gracz wykonujący skok
                multiply: O ile silniejszy ma być skok
                force_jump: Czy wymusić skok (jump_orb)
        """
        self._validate_player(player)

        if not (player.on_ground or force_jump):
            return

        # Skalowanie siły skoku na podstawie obecnej wysokości ekranu
        screen_height = pygame.display.get_surface().get_height()
        scaled_jump_force = (self.jump_force * multiply) * (screen_height / self.original_screen_height)

        player.velocity_y = scaled_jump_force
        player.on_ground = False

    """Sprawdza kolizję gracza z górną częścią bloków."""
    def _check_block_collision_top(self, player: Player, new_y: float) -> Optional[float]:
        """ Args:
                player: Gracz do sprawdzenia
                new_y: Nowa pozycja Y gracza
            Returns:
                Pozycja Y górnej części najwyższego bloku albo None
        """
        player_bottom = new_y + config.PLAYER_OUTER_SIZE // 2
        player_left = player.x - config.PLAYER_OUTER_SIZE // 2
        player_right = player.x + config.PLAYER_OUTER_SIZE // 2

        highest_block_top = None

        for obj in self.objects:
            if not isinstance(obj, Block):
                continue

            block_bounds = self._get_block_bounds(obj)

            # Czy gracz jest w poziomym zasięgu bloku
            if player_right >= block_bounds['left'] and player_left <= block_bounds['right']:

                # Spadanie na blok
                if player.velocity_y >= 0:
                    if block_bounds['top'] <= player_bottom <= block_bounds['bottom']:
                        if highest_block_top is None or block_bounds['top'] < highest_block_top:
                            highest_block_top = block_bounds['top']

        return highest_block_top

    """Sprawdza kolizję gracza z bokami bloków podczas ruchu poziomego."""
    def _check_block_collision_horizontal(self, player: Player, new_x: float) -> bool:
        """ Args:
                player: Gracz do sprawdzenia
                new_x: Nowa pozycja X gracza
            Returns:
                True, jeśli wystąpiła kolizja; False, jeśli ta kolizja nie wystąpiła
        """
        player_bounds = self._get_player_bounds_at_x(player, new_x)

        for obj in self.objects:
            if not (isinstance(obj, Block) or isinstance(obj, Spike)):
                continue

            if isinstance(obj, Block):
                block_bounds = self._get_block_bounds(obj)
                if self._rectangles_overlap(player_bounds, block_bounds):
                    return True

            if isinstance(obj, Spike):
                if self._check_spike_collision(player, obj):
                    return True

        return False

    """Sprawdza czy gracz ma kolizję z kolcem."""
    def _check_spike_collision(self, player: Player, spike: Spike):
        """ Args:
                player: Gracz
                spike: Kolec
            Returns:
                True, jeśli jakiś wierzchołek gracza jest w trójkącie; False w przeciwnym wypadku
        """
        spike.update_size(pygame.display.get_surface())
        points = spike.outer_points

        vertices = [
            self.screen_to_world(player.outer_rect.topleft),
            self.screen_to_world(player.outer_rect.topright),
            self.screen_to_world(player.outer_rect.bottomleft),
            self.screen_to_world(player.outer_rect.bottomright)
        ]

        for vertex in vertices:
            if self._is_point_inside_triangle(points, vertex):
                return True

        return False

    """Sprawdza czy punkt jest w trójkącie."""
    @staticmethod
    def _is_point_inside_triangle(points: list[tuple[int, int]], point: tuple[int, int]) -> bool:
        """ Args:
                points: Wierzchołki trójkąta
                point: Punkt
            Returns:
                True, jeśli punkt jest w trójkącie; False w przeciwnym wypadku
        """
        Engine._validate_triangle_points(points)

        x, y = point
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]

        A = Engine._get_triangle_area([(x1, y1), (x2, y2), (x3, y3)])

        A1 = Engine._get_triangle_area([(x, y), (x2, y2), (x3, y3)])

        A2 = Engine._get_triangle_area([(x1, y1), (x, y), (x3, y3)])

        A3 = Engine._get_triangle_area([(x1, y1), (x2, y2), (x, y)])

        return A == A1 + A2 + A3

    """Zwraca pole trójkąta."""
    @staticmethod
    def _get_triangle_area(points: list[tuple[int, int]]):
        """ Args:
                points: Wierzchołki trójkąta
            Returns:
                Pole trójkąta
        """
        Engine._validate_triangle_points(points)

        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]

        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

    """Zwraca granice gracza dla danej pozycji X."""
    @staticmethod
    def _get_player_bounds_at_x(player: Player, x: float) -> dict:
        """ Args:
                player: Gracz
                x: Pozycja X
            Returns:
                Słownik z granicami gracza
        """
        half_size = config.PLAYER_OUTER_SIZE // 2
        return {
            'left': x - half_size,
            'right': x + half_size,
            'top': player.y - half_size,
            'bottom': player.y + half_size
        }

    """Zwraca granice bloku."""
    @staticmethod
    def _get_block_bounds(block: Block) -> dict:
        """ Args:
                block: Blok do sprawdzenia
            Returns:
                Słownik z granicami bloku
        """
        half_size = config.BLOCK_OUTER_SIZE // 2
        return {
            'left': block.x - half_size,
            'right': block.x + half_size,
            'top': block.y - half_size,
            'bottom': block.y + half_size
        }

    """Sprawdza czy dwa prostokąty się nakładają."""
    @staticmethod
    def _rectangles_overlap(rect1: dict, rect2: dict) -> bool:
        """ Args:
                rect1: Pierwszy prostokąt
                rect2: Drugi prostokąt
            Returns:
                True, jeśli prostokąty się nakładają; False w przeciwnym wypadku
        """
        return (rect1['right'] > rect2['left'] and
                rect1['left'] < rect2['right'] and
                rect1['bottom'] > rect2['top'] and
                rect1['top'] < rect2['bottom'])

    """Resetuje gracza do pozycji startowej."""
    def reset_player(self, player: Player):
        """ Args:
                player: Gracz do zresetowania
        """
        self._validate_player(player)

        player.x = 90
        player.y = self.floor.floor_y - player.outer_size // 2
        player.velocity_y = 0
        player.on_ground = True
        self.camera_offset_x = 0

    """Stosuje grawitację do gracza."""
    def _apply_gravity(self, player: Player, delta_time: float):
        """ Args:
                player: Gracz, na którego działa grawitacja
                delta_time: Czas od ostatniej klatki
        """
        screen_height = pygame.display.get_surface().get_height()
        scaled_gravity = self.gravity * (screen_height / self.original_screen_height)
        player.velocity_y += scaled_gravity * delta_time

    """Tworzy obiekty gry na podstawie układu poziomu."""
    def set_objects_from_layout(self, layout: List[dict]):
        """ Args:
                layout: Lista słowników opisujących obiekty
        """
        self._validate_layout(layout)

        type_map = {
            "block": Block,
            "spike": Spike,
            "jump_pad": JumpPad,
            "jump_orb": JumpOrb
        }

        self.objects = []
        for obj_data in layout:
            obj_type = obj_data.get("type")
            if obj_type in type_map:
                obj_class = type_map[obj_type]
                obj = obj_class(obj_data["x"], obj_data["y"])
                self.objects.append(obj)

    """Rysuje wszystkie obiekty na ekranie z uwzględnieniem przesunięcia kamery."""
    def draw_objects(self, screen: pygame.Surface):
        """
            Args:
                screen: Powierzchnia do rysowania
        """
        self._validate_screen(screen)

        # Rysowanie tylko obiektów widocznych na ekranie
        for obj in self.objects:
            screen_x = obj.x + self.camera_offset_x

            if not self._is_object_visible(screen_x):
                continue

            self._draw_single_object(obj, screen, screen_x)

        if self.end_wall:
            self.end_wall.draw(screen)

    """Sprawdza czy obiekt jest widoczny na ekranie."""
    @staticmethod
    def _is_object_visible(screen_x: float) -> bool:
        """ Args:
                screen_x: Pozycja X obiektu na ekranie
            Returns:
                True, jeśli obiekt jest widoczny; False w przeciwnym wypadku
        """
        return -config.RENDER_MARGIN < screen_x < config.SCREEN_WIDTH + config.RENDER_MARGIN

    """Rysuje pojedynczy obiekt na ekranie."""
    @staticmethod
    def _draw_single_object(obj, screen: pygame.Surface, screen_x: float):
        """ Args:
                obj: Obiekt do narysowania
                screen: Powierzchnia do rysowania
                screen_x: Pozycja X obiektu na ekranie
        """
        obj_type = obj.__class__.__name__

        types = {
            "Block": Block(screen_x, obj.y),
            "Spike": Spike(screen_x, obj.y),
            "JumpOrb": JumpOrb(screen_x, obj.y),
            "JumpPad": JumpPad(screen_x, obj.y)
        }

        types[obj_type].draw(screen)

    """Konwertuje współrzędne świata na współrzędne ekranu."""
    def world_to_screen(self, world_pos: Tuple[int, int]) -> Tuple[int, int]:
        """ Args:
                world_pos: Pozycja w świecie (x, y)
            Returns:
                Pozycja na ekranie (x, y)
        """
        self._validate_world_pos(world_pos)
        x, y = world_pos
        return x + self.camera_offset_x, y

    """Konwertuje współrzędne ekranu na współrzędne świata."""
    def screen_to_world(self, screen_pos: Tuple[int, int]) -> Tuple[int, int]:
        """ Args:
                screen_pos: Pozycja w świecie (x, y)
            Returns:
                Pozycja na ekranie (x, y)
        """
        assert isinstance(screen_pos, tuple) and all(isinstance(x, int) for x in screen_pos), "screen_pos musi być krotką 2 liczb całkowitych"
        x, y = screen_pos
        return x - self.camera_offset_x, y

    """Zwraca pozycję X najdalszego obiektu w poziomie."""
    def get_furthest_object_x(self) -> float:
        """ Returns:
                Pozycja X najdalszego obiektu
        """
        furthest_x = 0

        for obj in self.objects:
            if obj.x > furthest_x:
                furthest_x = obj.x

        # Jeśli nie ma żadnych obiektów, minimalna długość poziomu
        if furthest_x == 0:
            furthest_x = config.MIN_LEVEL_LENGTH

        return furthest_x + config.END_WALL_X

    """Sprawdza kolizję gracza z przeszkodą."""
    @staticmethod
    def check_player_collision_with_object(player: Player, obstacle_rect: pygame.Rect) -> bool:
        """ Args:
                player: Gracz do sprawdzenia
                obstacle_rect: Prostokąt przeszkody
            Returns:
                True, jeśli wystąpiła kolizja; False w przeciwnym wypadku
        """
        Engine._validate_player(player)
        Engine._validate_obstacle_rect(obstacle_rect)
        return player.outer_rect.colliderect(obstacle_rect)

    """Sprawdza czy gracz dotknął podłoża."""
    def check_player_collision_with_floor(self, player: Player, screen: pygame.Surface) -> bool:
        """ Args:
                player: Gracz do sprawdzenia
                screen: Powierzchnia ekranu
            Returns:
                True, jeśli gracz dotknął podłoża
        """
        self._validate_player_screen(player, screen)
        return player.outer_rect.bottom >= self.floor.get_screen_floor_y(screen)

    # Funkcje walidacyjne
    @staticmethod
    def _validate_floor(floor):
        if not isinstance(floor, Floor):
            raise ValueError("floor musi być instancją klasy Floor")

    @staticmethod
    def _validate_player(player):
        if not isinstance(player, Player):
            raise ValueError("player musi być instancją klasy Player")

    @staticmethod
    def _validate_update_params(player, delta_time, screen):
        Engine._validate_player(player)
        if not isinstance(delta_time, float) or delta_time <= 0:
            raise ValueError("delta_time musi być dodatnią liczbą zmiennoprzecinkową")
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")

    @staticmethod
    def _validate_layout(layout):
        if not isinstance(layout, list):
            raise ValueError("layout musi być listą")

    @staticmethod
    def _validate_screen(screen):
        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen musi być instancją pygame.Surface")

    @staticmethod
    def _validate_world_pos(world_pos):
        if not isinstance(world_pos, tuple) or len(world_pos) != 2 or not all(isinstance(x, int) for x in world_pos):
            raise ValueError("world_pos musi być krotką 2 liczb całkowitych")

    @staticmethod
    def _validate_obstacle_rect(obstacle_rect):
        if not isinstance(obstacle_rect, pygame.Rect):
            raise ValueError("obstacle_rect musi być instancją pygame.Rect")

    @staticmethod
    def _validate_triangle_points(points):
        if not isinstance(points, list) and not all(isinstance(x, tuple) for x in points) and not length(points) == 3:
            raise ValueError("points musi być listą krotek")

    @staticmethod
    def _validate_player_screen(player, screen):
        Engine._validate_player(player)
        Engine._validate_screen(screen)

    @staticmethod
    def _validate_game_over_params(player, obstacles):
        Engine._validate_player(player)
        if not isinstance(obstacles, list) or not all(isinstance(rect, pygame.Rect) for rect in obstacles):
            raise ValueError("obstacles musi być listą obiektów pygame.Rect")