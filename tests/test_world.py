import json

import pytest

from scripts.camera import CameraModel
from scripts.field import FieldModel
from scripts.world import WorldModel


def make_world(x=0, y=0, distance=10, resolution=(1000, 500)):
    camera = CameraModel(x=x, y=y, distance=distance, resolution=resolution)
    return WorldModel(camera_model=camera)


def test_default_models_are_created():
    world = WorldModel()

    assert isinstance(world.camera_model, CameraModel)
    assert isinstance(world.field_model, FieldModel)


def test_injected_models_are_used():
    camera = CameraModel(x=1, y=2, distance=3, resolution=(800, 600))

    world = WorldModel(camera_model=camera)

    assert world.camera_model is camera


def test_step_left_decreases_x():
    world = make_world(x=5, distance=10)

    world.step(1000, ["left"])

    assert world.camera_model.x == pytest.approx(-5)


def test_step_right_increases_x():
    world = make_world(x=5, distance=10)

    world.step(1000, ["right"])

    assert world.camera_model.x == pytest.approx(15)


def test_step_up_decreases_y():
    world = make_world(y=5, distance=10)

    world.step(1000, ["up"])

    assert world.camera_model.y == pytest.approx(-5)


def test_step_down_increases_y():
    world = make_world(y=5, distance=10)

    world.step(1000, ["down"])

    assert world.camera_model.y == pytest.approx(15)


def test_step_zoom_in_increases_distance():
    world = make_world(distance=10)

    world.step(1000, ["zoom_in"])

    assert world.camera_model.distance == pytest.approx(20)


def test_step_zoom_out_decreases_distance():
    world = make_world(distance=10)

    world.step(1000, ["zoom_out"])

    assert world.camera_model.distance == pytest.approx(0)


def test_step_applies_multiple_intents():
    world = make_world(x=0, y=0, distance=10)

    world.step(1000, ["right", "down"])

    assert world.camera_model.x == pytest.approx(10)
    assert world.camera_model.y == pytest.approx(10)


def test_step_without_intents_does_not_move():
    world = make_world(x=5, y=6, distance=10)
    before = (world.camera_model.x, world.camera_model.y, world.camera_model.distance)

    world.step(1000, [])

    assert (world.camera_model.x, world.camera_model.y, world.camera_model.distance) == before


def test_step_ignores_unknown_intents():
    world = make_world(x=5, distance=10)

    world.step(1000, ["fly", "left"])

    assert world.camera_model.x == pytest.approx(-5)


def test_step_accepts_any_iterable():
    world = make_world(x=0, distance=10)

    world.step(1000, {"right"})

    assert world.camera_model.x == pytest.approx(10)


def test_step_is_frame_rate_independent():
    fast = make_world(x=0, distance=10)
    slow = make_world(x=0, distance=10)

    fast.step(500, ["right"])
    fast.step(500, ["right"])
    slow.step(1000, ["right"])

    assert fast.camera_model.x == pytest.approx(slow.camera_model.x)


def test_snapshot_contains_camera_and_field():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))

    snapshot = world.snapshot()

    assert snapshot == {
        "camera": {"x": 1, "y": 2, "distance": 3, "resolution": [800, 600]},
        "field": {},
    }


def test_snapshot_roundtrip():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    other = make_world(x=0, y=0, distance=1, resolution=(640, 480))

    other.apply_snapshot(world.snapshot())

    assert other.camera_model.x == 1
    assert other.camera_model.y == 2
    assert other.camera_model.distance == 3
    assert other.camera_model.resolution == (800, 600)


def test_apply_snapshot_mutates_existing_models():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    camera = world.camera_model

    world.apply_snapshot(world.snapshot())

    assert world.camera_model is camera


def test_snapshot_is_json_serializable():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))

    assert json.loads(json.dumps(world.snapshot())) == world.snapshot()
