import json

import pytest

from scripts.camera import CameraModel
from scripts.field import FieldModel
from scripts.world import WorldModel


def make_world(x=0, y=0, distance=10, resolution=(1000, 500)):
    camera = CameraModel(x=x, y=y, distance=distance, resolution=resolution)
    world = WorldModel(camera_model=camera)
    world.add_player(0)
    return world


def test_default_models_are_created():
    world = WorldModel()

    assert isinstance(world.camera_model, CameraModel)
    assert isinstance(world.field_model, FieldModel)
    assert world.players == {}


def test_injected_models_are_used():
    camera = CameraModel(x=1, y=2, distance=3, resolution=(800, 600))

    world = WorldModel(camera_model=camera)

    assert world.camera_model is camera


def test_add_player_returns_model():
    world = WorldModel()

    player = world.add_player("0")

    assert world.players["0"] is player


def test_remove_player():
    world = WorldModel()
    world.add_player("0")

    world.remove_player("0")

    assert world.players == {}


def test_remove_missing_player_is_safe():
    world = WorldModel()

    world.remove_player(99)

    assert world.players == {}


def test_step_left_moves_player_left():
    world = make_world()

    world.step(1000, ["left"])

    assert world.players["0"].x == pytest.approx(-1)
    assert world.camera_model.x == 0


def test_step_right_moves_player_right():
    world = make_world()

    world.step(1000, ["right"])

    assert world.players["0"].x == pytest.approx(1)
    assert world.camera_model.x == 0


def test_step_up_moves_player_up():
    world = make_world()

    world.step(1000, ["up"])

    assert world.players["0"].y == pytest.approx(-1)
    assert world.camera_model.y == 0


def test_step_down_moves_player_down():
    world = make_world()

    world.step(1000, ["down"])

    assert world.players["0"].y == pytest.approx(1)
    assert world.camera_model.y == 0


def test_step_zoom_in_increases_distance():
    world = make_world(distance=10)

    world.step(1000, ["zoom_in"])

    assert world.camera_model.distance == pytest.approx(20)


def test_step_zoom_out_decreases_distance():
    world = make_world(distance=10)

    world.step(1000, ["zoom_out"])

    assert world.camera_model.distance == pytest.approx(0)


def test_step_applies_multiple_intents():
    world = make_world()

    world.step(1000, ["right", "down"])

    assert world.players["0"].x == pytest.approx(1)
    assert world.players["0"].y == pytest.approx(1)


def test_step_without_intents_does_not_move():
    world = make_world()
    before = (world.players["0"].x, world.players["0"].y)

    world.step(1000, [])

    assert (world.players["0"].x, world.players["0"].y) == before


def test_step_ignores_unknown_intents():
    world = make_world()

    world.step(1000, ["fly", "left"])

    assert world.players["0"].x == pytest.approx(-1)


def test_step_accepts_any_iterable():
    world = make_world()

    world.step(1000, {"right"})

    assert world.players["0"].x == pytest.approx(1)


def test_step_is_frame_rate_independent():
    fast = make_world()
    slow = make_world()

    fast.step(500, ["right"])
    fast.step(500, ["right"])
    slow.step(1000, ["right"])

    assert fast.players["0"].x == pytest.approx(slow.players["0"].x)


def test_step_players_uses_per_player_intents():
    world = make_world()
    world.add_player(1)

    world.step_players(1000, {"0": {"right"}, "1": {"left"}})

    assert world.players["0"].x == pytest.approx(1)
    assert world.players["1"].x == pytest.approx(-1)


def test_step_players_ignores_unknown_players():
    world = make_world()

    world.step_players(1000, {"99": {"right"}})

    assert world.players["0"].x == pytest.approx(0)


def test_snapshot_contains_camera_field_and_players():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    world.players["0"].color = (10, 20, 30)

    snapshot = world.snapshot()

    assert snapshot["camera"] == {"x": 1, "y": 2, "distance": 3, "resolution": [800, 600]}
    assert snapshot["field"] == {}
    assert snapshot["players"] == {"0": {"x": 0, "y": 0, "color": [10, 20, 30], "size": 2}}


def test_snapshot_roundtrip():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    other = WorldModel(camera_model=CameraModel(x=0, y=0, distance=1, resolution=(640, 480)))

    other.apply_snapshot(world.snapshot())

    assert other.camera_model.x == 1
    assert other.camera_model.y == 2
    assert other.camera_model.distance == 3
    assert other.camera_model.resolution == (800, 600)
    assert list(other.players) == ["0"]


def test_apply_snapshot_creates_and_removes_players():
    world = make_world()
    world.add_player(1)
    other = WorldModel()

    other.apply_snapshot(world.snapshot())

    assert set(other.players) == {"0", "1"}


def test_apply_players_snapshot_keeps_model_identity():
    world = WorldModel()
    player = world.add_player("0")

    world.apply_players_snapshot({"0": {"x": 5, "y": 6, "color": [1, 2, 3], "size": 2}})

    assert world.players["0"] is player
    assert world.players["0"].x == 5


def test_snapshot_survives_json_roundtrip_keys():
    world = make_world()
    other = WorldModel()

    serialized = json.loads(json.dumps(world.snapshot()))
    other.apply_snapshot(serialized)

    assert list(other.players) == ["0"]
    assert other.players["0"].to_dict() == world.players["0"].to_dict()


def test_apply_snapshot_mutates_existing_models():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))
    camera = world.camera_model

    world.apply_snapshot(world.snapshot())

    assert world.camera_model is camera


def test_snapshot_is_json_serializable():
    world = make_world(x=1, y=2, distance=3, resolution=(800, 600))

    assert json.loads(json.dumps(world.snapshot())) == world.snapshot()
