import pygame
import pytest

from scripts.app import App
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldModel, FieldView
from scripts.net.client import Client, LocalClient
from scripts.world import WorldModel


class FakeKeys:
    def __init__(self, pressed=()):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed


@pytest.fixture
def app():
    return App()


def test_app_wires_models_and_views(app):
    assert isinstance(app.world, WorldModel)
    assert isinstance(app.camera_model, CameraModel)
    assert isinstance(app.camera_view, CameraView)
    assert isinstance(app.field_model, FieldModel)
    assert isinstance(app.field_view, FieldView)


def test_app_uses_a_local_client_by_default(app):
    assert isinstance(app.client, Client)
    assert isinstance(app.client, LocalClient)
    assert app.client.world is app.world


def test_app_uses_injected_client():
    world = WorldModel()
    client = LocalClient(world)

    app = App(client=client)

    assert app.client is client


def test_view_shares_the_same_model(app):
    assert app.camera_view.model is app.camera_model
    assert app.field_view.model is app.field_model


def test_app_models_belong_to_the_world(app):
    assert app.camera_model is app.world.camera_model
    assert app.field_model is app.world.field_model


def test_collect_intents_maps_keys_to_actions(app):
    app.keys = FakeKeys([pygame.K_a, pygame.K_e])

    assert app.collect_intents() == {"left", "zoom_in"}


def test_collect_intents_empty_without_keys(app):
    app.keys = FakeKeys()

    assert app.collect_intents() == set()


def test_physics_moves_camera_left(app):
    app.dt = 1000
    app.camera_model.distance = 10
    app.camera_model.x = 5
    app.keys = FakeKeys([pygame.K_a])
    app.intents = app.collect_intents()

    app.update_physics()

    assert app.camera_model.x < 5


def test_physics_moves_camera_right(app):
    app.dt = 1000
    app.camera_model.distance = 10
    app.camera_model.x = 5
    app.keys = FakeKeys([pygame.K_d])
    app.intents = app.collect_intents()

    app.update_physics()

    assert app.camera_model.x == pytest.approx(15)


def test_physics_does_not_move_without_keys(app):
    app.dt = 1000
    app.keys = FakeKeys()
    app.intents = app.collect_intents()
    before = (app.camera_model.x, app.camera_model.y, app.camera_model.distance)

    app.update_physics()

    assert (app.camera_model.x, app.camera_model.y, app.camera_model.distance) == before


def test_physics_scales_in_and_out(app):
    app.dt = 1000
    app.camera_model.distance = 10
    app.keys = FakeKeys([pygame.K_e])
    app.intents = app.collect_intents()
    app.update_physics()
    assert app.camera_model.distance > 10

    app.camera_model.distance = 10
    app.keys = FakeKeys([pygame.K_q])
    app.intents = app.collect_intents()
    app.update_physics()
    assert app.camera_model.distance < 10


def test_physics_applies_snapshot_from_client():
    class NullClient(Client):
        def update(self, dt, intents):
            return {"camera": {"x": 42, "y": 0, "distance": 5, "resolution": [1080, 720]},
                    "field": {}}

        def close(self):
            pass

    app = App(client=NullClient())
    app.dt = 1000
    app.intents = set()

    app.update_physics()

    assert app.camera_model.x == 42
    assert app.camera_model.distance == 5


def test_physics_ignores_none_snapshot():
    class IdleClient(Client):
        def update(self, dt, intents):
            return None

        def close(self):
            pass

    app = App(client=IdleClient())
    app.dt = 1000
    app.camera_model.x = 7
    app.intents = set()

    app.update_physics()

    assert app.camera_model.x == 7


def test_update_runs_all_blocks(app):
    app.dt = 1000
    app.keys = FakeKeys()

    app.update()

    assert app.mouse_pos is not None
