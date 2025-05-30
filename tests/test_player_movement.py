import pytest
import pygame

from unittest.mock import Mock, patch

from game.engine import Engine
from game.player import Player
from game.floor import Floor

from config import config

class TestPlayerMovement:
    @pytest.fixture
    def setup(self):
        floor = Mock(spec=Floor)
        floor.floor_y = config.FLOOR_Y
        floor.get_screen_floor_y.return_value = floor.floor_y

        engine = Engine(floor)

        player = Mock(spec=Player)
        player.x = config.PLAYER_START_X
        player.y = config.FLOOR_Y - config.PLAYER_OUTER_SIZE // 2
        player.velocity_y = 0
        player.rotation = 0
        player.on_ground = True
        player.outer_rect = pygame.Rect(player.x, player.y, config.PLAYER_OUTER_SIZE, config.PLAYER_OUTER_SIZE)

        screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        return engine, player, floor, screen

    def test_player_jump_when_on_ground(self, setup):
        engine, player, _, _ = setup

        with patch('pygame.display.get_surface') as mock_surface:
            mock_surface.return_value.get_height.return_value = 600

            engine.player_jump(player)

            assert player.velocity_y < 0
            assert not player.on_ground

    def test_player_jump_when_in_air(self, setup):
        engine, player, _, _ = setup

        player.on_ground = False
        original_velocity = player.velocity_y

        engine.player_jump(player)

        assert player.velocity_y == original_velocity  # Brak zmiany prędkości
        assert not player.on_ground

    def test_player_jump_with_invalid_player(self, setup):
        engine, _, _, _ = setup

        with pytest.raises(ValueError, match="player musi być instancją klasy Player"):
            engine.player_jump("not_a_player")

    def test_horizontal_movement_no_collision(self, setup):
        engine, player, _, screen = setup
        delta_time = 0.016

        with patch('pygame.display.get_surface', return_value=screen):
            with patch.object(engine, '_check_block_collision_horizontal', return_value=False):
                with patch.object(engine, '_apply_gravity'):
                    with patch.object(engine, '_update_vertical_movement', return_value=False):
                        with patch.object(engine, '_update_camera'):
                            game_over = engine.update_player(player, delta_time, screen)
                            assert not game_over

    def test_horizontal_movement_with_collision(self, setup):
        engine, player, _, screen = setup
        delta_time = 0.016

        with patch.object(engine, '_check_block_collision_horizontal', return_value=True):
            with patch.object(engine, '_apply_gravity'):
                with patch.object(engine, '_update_vertical_movement', return_value=False):
                    game_over = engine.update_player(player, delta_time, screen)
                    assert game_over

    def test_vertical_movement_with_collision(self, setup):
        engine, player, _, screen = setup
        delta_time = 0.016

        with patch('pygame.display.get_surface', return_value=screen):
            with patch.object(engine, '_check_block_collision_horizontal', return_value=False):
                with patch.object(engine, '_apply_gravity'):
                    with patch.object(engine, '_update_vertical_movement', return_value=True):
                        with patch.object(engine, '_update_camera'):
                            game_over = engine.update_player(player, delta_time, screen)
                            assert game_over

    def test_movement_with_both_collisions(self, setup):
        engine, player, _, screen = setup
        delta_time = 0.016

        with patch.object(engine, '_check_block_collision_horizontal', return_value=True):
            with patch.object(engine, '_apply_gravity'):
                with patch.object(engine, '_update_vertical_movement', return_value=True):
                    game_over = engine.update_player(player, delta_time, screen)
                    assert game_over