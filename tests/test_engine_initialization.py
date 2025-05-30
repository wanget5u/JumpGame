import pytest
import pygame

from unittest.mock import Mock, patch

from game.engine import Engine
from game.floor import Floor

class TestEngineInitialization:
    def test_engine_init_with_valid_floor(self):
        floor = Mock(spec=Floor)
        engine = Engine(floor)

        assert engine.floor == floor
        assert engine.gravity == 4500
        assert engine.jump_force == -1350
        assert engine.attempts == 1
        assert engine.objects == []
        assert engine.camera_offset_x == 0
        assert engine.end_wall is None

    def test_engine_init_with_invalid_floor(self):
        with pytest.raises(ValueError, match="floor musi być instancją klasy Floor"):
            Engine("not_a_floor")

    def test_engine_init_with_none_floor(self):
        with pytest.raises(ValueError, match="floor musi być instancją klasy Floor"):
            Engine(None)