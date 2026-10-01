import json

import pytest

from scripts.camera import CameraModel


def make_camera(x=0, y=0, distance=10, resolution=(1000, 500)):
    return CameraModel(x=x, y=y, distance=distance, resolution=resolution)


def test_constructor_stores_state():
    camera = make_camera(x=3, y=4, distance=8, resolution=(800, 600))

    assert camera.x == 3
    assert camera.y == 4
    assert camera.distance == 8
    assert camera.resolution == (800, 600)


def test_get_local_point_scales_global_coordinates():
    camera = make_camera(x=0, y=0, distance=10, resolution=(1000, 500))

    assert camera.get_local_point(10, 5) == (1000.0, 500.0)


def test_get_local_point_applies_camera_offset():
    camera = make_camera(x=2, y=3, distance=10, resolution=(1000, 500))

    assert camera.get_local_point(2, 3) == (0.0, 0.0)


def test_get_global_point_is_inverse_of_local_point():
    camera = make_camera(x=2, y=3, distance=10, resolution=(1000, 500))

    local = camera.get_local_point(7, 9)
    global_point = camera.get_global_point(*local)

    assert global_point == pytest.approx((7, 9))


def test_get_local_radius_scales_radius_by_zoom():
    camera = make_camera(distance=10, resolution=(1000, 500))

    assert camera.get_local_radius(2) == 200.0


def test_get_global_radius_is_inverse_of_local_radius():
    camera = make_camera(distance=10, resolution=(1000, 500))

    local = camera.get_local_radius(3)
    global_radius = camera.get_global_radius(local)

    assert local == 300.0
    assert global_radius == pytest.approx(3.0)


def test_get_global_radius_scales_radius_by_zoom():
    camera = make_camera(distance=10, resolution=(1000, 500))

    assert camera.get_global_radius(200) == pytest.approx(2.0)


def test_move_left_decreases_x():
    camera = make_camera(x=5, distance=10)

    camera.move_left(1, 1000)

    assert camera.x == pytest.approx(5 - 1 * 10 * 1000 / 1000)


def test_move_right_increases_x():
    camera = make_camera(x=5, distance=10)

    camera.move_right(2, 500)

    assert camera.x == pytest.approx(5 + 2 * 10 * 500 / 1000)


def test_move_up_decreases_y():
    camera = make_camera(y=5, distance=10)

    camera.move_up(1, 1000)

    assert camera.y == pytest.approx(5 - 10)


def test_move_down_increases_y():
    camera = make_camera(y=5, distance=10)

    camera.move_down(1, 1000)

    assert camera.y == pytest.approx(5 + 10)


def test_movement_is_frame_rate_independent():
    fast = make_camera(x=0, distance=10)
    slow = make_camera(x=0, distance=10)

    fast.move_right(1, 500)
    fast.move_right(1, 500)
    slow.move_right(1, 1000)

    assert fast.x == pytest.approx(slow.x)


def test_scale_in_increases_distance():
    camera = make_camera(distance=10)

    camera.scale_in(1, 1000)

    assert camera.distance == pytest.approx(10 + 10 * 1 * 1000 / 1000)


def test_scale_out_decreases_distance():
    camera = make_camera(distance=10)

    camera.scale_out(1, 1000)

    assert camera.distance == pytest.approx(10 - 10 * 1 * 1000 / 1000)


def test_scale_is_proportional_to_current_distance():
    camera = make_camera(distance=100)

    camera.scale_in(1, 500)

    assert camera.distance == pytest.approx(100 * 1.5)


def test_to_dict_returns_state():
    camera = make_camera(x=3, y=4, distance=8, resolution=(800, 600))

    assert camera.to_dict() == {
        "x": 3,
        "y": 4,
        "distance": 8,
        "resolution": [800, 600],
    }


def test_from_dict_restores_state():
    camera = make_camera(x=0, y=0, distance=1, resolution=(640, 480))

    camera.from_dict({"x": 7, "y": 9, "distance": 12, "resolution": [800, 600]})

    assert camera.x == 7
    assert camera.y == 9
    assert camera.distance == 12
    assert camera.resolution == (800, 600)


def test_snapshot_roundtrip():
    original = make_camera(x=3, y=4, distance=8, resolution=(800, 600))
    restored = make_camera(x=0, y=0, distance=1, resolution=(640, 480))

    restored.from_dict(original.to_dict())

    assert restored.x == original.x
    assert restored.y == original.y
    assert restored.distance == original.distance
    assert restored.resolution == original.resolution


def test_dict_is_json_serializable():
    camera = make_camera(x=3, y=4, distance=8, resolution=(800, 600))

    assert json.loads(json.dumps(camera.to_dict())) == camera.to_dict()
