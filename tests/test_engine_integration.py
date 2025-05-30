import pytest
import pygame

from unittest.mock import Mock, patch

from game.engine import Engine
from game.player import Player
from game.floor import Floor

from config import config

class TestEngineIntegration:
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

    def test_complete_game_loop_cycle(self, setup):
        engine, player, floor, screen = setup
        delta_time = 0.016
        game_over = True

        for _ in range(10):
            with patch('pygame.display.get_surface', return_value=screen):
                game_over = engine.update_player(player, delta_time, screen)

        assert not game_over

    def test_player_jump_and_landing_sequence(self, setup):
        engine, player, floor, screen = setup
        delta_time = 0.016
        game_over = True

        assert player.on_ground

        with patch('pygame.display.get_surface', return_value=screen):
            engine.player_jump(player)

            assert not player.on_ground
            assert player.velocity_y < 0

            for _ in range(60):
                with patch.object(engine, '_check_block_collision_horizontal', return_value=False):
                    with patch.object(engine, '_check_block_collision_top', return_value=None):
                        game_over = engine.update_player(player, delta_time, screen)

                if player.on_ground:
                    break

            assert not game_over
            assert player.on_ground
            assert abs(player.velocity_y) < 0.1  # Prędkość bliska zeru

    def test_block_collision_and_landing(self, setup):
        engine, player, floor, screen = setup
        delta_time = 0.016

        block = Mock()
        block.x, block.y = 120, 480
        engine.objects = [block]

        player.velocity_y = 100
        player.x, player.y = 120, 420
        player.on_ground = False

        game_over = True

        for _ in range(20):
            with patch('pygame.display.get_surface', return_value=screen):
                game_over = engine.update_player(player, delta_time, screen)

        assert not game_over
        assert player.on_ground
        assert abs(player.velocity_y) < 0.1

    def test_camera_following_player(self, setup):
        engine, player, floor, screen = setup
        delta_time = 0.016
        player.x = 120
        game_over = True

        expected_camera_offset_x = 0

        for _ in range(20):
            with patch('pygame.display.get_surface', return_value=screen):
                game_over = engine.update_player(player, delta_time, screen)
                expected_camera_offset_x = -(player.x - config.SCREEN_WIDTH // 6)

        assert not game_over
        assert engine.camera_offset_x == int(expected_camera_offset_x)

    def test_level_layout_loading_and_rendering(self, setup):
        engine, player, floor, screen = setup

        layout = [
            {"type": "block", "x": 330, "y": 390},
            {"type": "spike", "x": 330, "y": 450},
            {"type": "jump_pad", "x": 330, "y": 490}
        ]

        with patch('game.engine.Block') as mock_block, \
                patch('game.engine.Spike') as mock_spike, \
                patch('game.engine.JumpPad') as mock_jump_pad:
            engine.set_objects_from_layout(layout)

        assert len(engine.objects) == 3
        mock_block.assert_called_once_with(330, 390)
        mock_spike.assert_called_once_with(330, 450)
        mock_jump_pad.assert_called_once_with(330, 490)

    @patch('config.config.MIN_LEVEL_LENGTH', 1020)
    @patch('config.config.END_WALL_X', 120)
    def test_end_wall_positioning(self, setup):
        engine, player, floor, screen = setup

        # Dodaj obiekty na różnych pozycjach X
        objects_data = [
            {"type": "block", "x": 330, "y": 390},
            {"type": "block", "x": 390, "y": 390},
            {"type": "block", "x": 450, "y": 390}
        ]

        with patch('objects.block.Block'):
            engine.set_objects_from_layout(objects_data)
            furthest_x = engine.get_furthest_object_x()

            assert furthest_x == 570

        objects_data = []

        with patch('objects.block.Block'):
            engine.set_objects_from_layout(objects_data)
            furthest_x = engine.get_furthest_object_x()

            assert furthest_x == 1140