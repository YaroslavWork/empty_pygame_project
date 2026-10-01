import json

import pytest

from scripts.player import PlayerModel, PlayerView
from scripts.player.model import get_random_color


def test_default_state_is_created():
    player = PlayerModel()

    assert player.x == 0
    assert player.y == 0
    assert len(player.color) == 3
    assert all(0 <= channel <= 255 for channel in player.color)
    assert player.size == 2


def test_injected_state_is_used():
    player = PlayerModel(x=1, y=2, color=(10, 20, 30), size=5)

    assert (player.x, player.y) == (1, 2)
    assert player.color == (10, 20, 30)
    assert player.size == 5


def test_move_left_decreases_x():
    player = PlayerModel(x=5)

    player.move_left(1, 1000)

    assert player.x == pytest.approx(4)


def test_move_right_increases_x():
    player = PlayerModel(x=5)

    player.move_right(1, 1000)

    assert player.x == pytest.approx(6)


def test_move_up_decreases_y():
    player = PlayerModel(y=5)

    player.move_up(1, 1000)

    assert player.y == pytest.approx(4)


def test_move_down_increases_y():
    player = PlayerModel(y=5)

    player.move_down(1, 1000)

    assert player.y == pytest.approx(6)


def test_movement_is_frame_rate_independent():
    fast = PlayerModel()
    slow = PlayerModel()

    fast.move_right(1, 500)
    fast.move_right(1, 500)
    slow.move_right(1, 1000)

    assert fast.x == pytest.approx(slow.x)


def test_to_dict_is_json_serializable():
    player = PlayerModel(x=1, y=2, color=(10, 20, 30), size=5)

    assert json.loads(json.dumps(player.to_dict())) == {
        "x": 1,
        "y": 2,
        "color": [10, 20, 30],
        "size": 5,
    }


def test_from_dict_restores_state():
    player = PlayerModel()

    player.from_dict({"x": 1, "y": 2, "color": [10, 20, 30], "size": 5})

    assert player.x == 1
    assert player.y == 2
    assert player.color == (10, 20, 30)
    assert player.size == 5


def test_roundtrip():
    player = PlayerModel(x=1, y=2, color=(10, 20, 30), size=5)
    other = PlayerModel()

    other.from_dict(player.to_dict())

    assert other.to_dict() == player.to_dict()


def test_random_colors_vary():
    colors = {get_random_color() for _ in range(50)}

    assert len(colors) > 1


def test_view_draws_player_rect(screen):
    from scripts.camera import CameraModel

    camera = CameraModel(x=0, y=0, distance=10, resolution=(320, 240))
    player = PlayerModel(x=0, y=0, color=(255, 0, 0), size=2)
    view = PlayerView(player)

    view.draw(screen, camera)

    center = camera.get_local_point(player.x, player.y)
    assert screen.get_at(tuple(map(int, center)))[:3] == (255, 0, 0)


def test_view_uses_camera_offset(screen):
    from scripts.camera import CameraModel

    camera = CameraModel(x=100, y=100, distance=10, resolution=(320, 240))
    player = PlayerModel(x=100, y=100, color=(0, 255, 0), size=2)
    view = PlayerView(player)

    view.draw(screen, camera)

    assert screen.get_at((0, 0))[:3] == (0, 255, 0)
