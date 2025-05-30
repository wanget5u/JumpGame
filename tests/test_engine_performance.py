import pytest
import pygame

from unittest.mock import Mock, patch

from game.engine import Engine
from game.player import Player
from game.floor import Floor

class TestEnginePerformance:
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

    """Test wydajności kolizji z wieloma obiektami."""
    def test_collision_detection_performance(self):
        floor = Mock(spec=Floor)
        engine = Engine(floor)

        many_objects = []
        for i in range(100):
            obj = Mock()
            obj.x = i * 50
            obj.y = 400
            many_objects.append(obj)

        engine.objects = many_objects

        player = Mock(spec=Player)
        player.x = 2520
        player.velocity_y = 0

        import time
        start_time = time.time()

        engine._check_block_collision_top(player, player.x)

        end_time = time.time()
        execution_time = end_time - start_time

        # Test powinien wykonać się w mniej niż 10ms
        assert execution_time < 0.01

    """Test wydajności renderowania z wieloma obiektami."""
    def test_rendering_performance_with_many_objects(self):
        floor = Mock(spec=Floor)
        engine = Engine(floor)
        engine.end_wall = Mock()

        many_objects = []
        for i in range(200):
            obj = Mock()
            obj.x = i * 60
            obj.y = 390
            obj.__class__.__name__ = 'Block'
            many_objects.append(obj)

        engine.objects = many_objects
        engine.camera_offset_x = -5000

        screen = pygame.Surface((800, 600))

        import time
        start_time = time.time()

        with patch('config.config.SCREEN_WIDTH', 800):
            with patch('objects.block.Block') as mock_block:
                mock_instance = Mock()
                mock_block.return_value = mock_instance

                engine.draw_objects(screen)

        end_time = time.time()
        execution_time = end_time - start_time

        assert execution_time < 0.05
        assert mock_block.call_count < 20