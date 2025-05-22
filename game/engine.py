import pygame

from config import config
from game.player import Player
from game.floor import Floor

class Engine:
    def __init__(self, floor: Floor):
        assert isinstance(floor, Floor), "floor musi być instancją klasy Floor"

        self.floor = floor
        self.gravity = 4500
        self.jump_force = -1350

        self.original_screen_height = config.SCREEN_HEIGHT
        self.original_screen_width = config.SCREEN_WIDTH

    def _check_player_coherence(self, player: Player) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        return player.outer_rect.bottom <= self.floor.floor_y

    """ Sprawdza kolizję gracza z przeszkodą """
    def check_player_collision_with_object(self, player: Player, obstacle_rect: pygame.Rect) -> bool:
        assert isinstance(player, Player), "player musi być instancją klasy Player"
        assert isinstance(obstacle_rect, pygame.Rect), "obstacle_rect musi być instancją pygame.Rect"
        return player.outer_rect.colliderect(obstacle_rect)

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