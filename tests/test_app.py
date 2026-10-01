import pygame
import pytest

from scripts import settings as s
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


def test_app_creates_a_local_player(app):
    assert list(app.world.players) == ["0"]


def test_app_does_not_create_a_player_for_remote_clients():
    class NullClient(Client):
        def update(self, dt, intents):
            return None

        def close(self):
            pass

    app = App(client=NullClient())

    assert app.world.players == {}


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


def test_physics_moves_player_left(app):
    app.dt = 1000
    app.keys = FakeKeys([pygame.K_a])
    app.intents = app.collect_intents()
    before = app.world.players["0"].x

    app.update_physics()

    assert app.world.players["0"].x < before


def test_physics_moves_player_right(app):
    app.dt = 1000
    app.keys = FakeKeys([pygame.K_d])
    app.intents = app.collect_intents()

    app.update_physics()

    assert app.world.players["0"].x == pytest.approx(s.PLAYER_MOVE_SPEED)


def test_physics_interpolates_player_render_position(app):
    app.dt = 1000
    app.keys = FakeKeys([pygame.K_d])
    app.intents = app.collect_intents()

    app.update_physics()

    # With a full second of dt the render position catches up to the state
    assert app.world.players["0"].render_x == pytest.approx(app.world.players["0"].x)


def test_physics_does_not_move_camera_with_wasd(app):
    app.dt = 1000
    app.keys = FakeKeys([pygame.K_d])
    app.intents = app.collect_intents()

    app.update_physics()

    assert app.camera_model.x == 0


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
                    "field": {},
                    "players": {"7": {"x": 1, "y": 2, "color": [10, 20, 30], "size": 2}}}

        def close(self):
            pass

    app = App(client=NullClient())
    app.dt = 1000
    app.intents = set()

    app.update_physics()

    assert app.camera_model.x == 42
    assert app.camera_model.distance == 5
    assert list(app.world.players) == ["7"]


def test_physics_keeps_local_resolution():
    class NullClient(Client):
        def update(self, dt, intents):
            return {"camera": {"x": 0, "y": 0, "distance": 5, "resolution": [640, 480]},
                    "field": {},
                    "players": {}}

        def close(self):
            pass

    app = App(client=NullClient())
    app.dt = 1000
    app.intents = set()

    app.update_physics()

    assert app.camera_model.resolution == tuple(app.size)


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


def test_draw_players_builds_views(app, screen):
    app.screen = screen

    app.draw_players()

    assert set(app.player_views) == set(app.world.players)


def test_draw_players_removes_missing_views(app, screen):
    app.screen = screen
    app.draw_players()
    app.world.remove_player(0)

    app.draw_players()

    assert app.player_views == {}


def test_update_runs_all_blocks(app):
    app.dt = 1000
    app.keys = FakeKeys()

    app.update()

    assert app.mouse_pos is not None
