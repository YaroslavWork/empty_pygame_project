import pygame
import pytest

from scripts.app import App
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldModel, FieldView


class FakeKeys:
    def __init__(self, pressed=()):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed


@pytest.fixture
def app():
    return App()


def test_app_wires_models_and_views(app):
    assert isinstance(app.camera_model, CameraModel)
    assert isinstance(app.camera_view, CameraView)
    assert isinstance(app.field_model, FieldModel)
    assert isinstance(app.field_view, FieldView)


def test_view_shares_the_same_model(app):
    assert app.camera_view.model is app.camera_model
    assert app.field_view.model is app.field_model


def test_physics_moves_camera_left(app):
    app.dt = 1000
    app.camera_model.distance = 10
    app.camera_model.x = 5
    app.keys = FakeKeys([pygame.K_a])

    app.update_physics()

    assert app.camera_model.x < 5


def test_physics_moves_camera_right(app):
    app.keys = FakeKeys([pygame.K_d])
    app.dt = 1000
    app.camera_model.distance = 10
    app.camera_model.x = 5

    app.update_physics()

    assert app.camera_model.x == pytest.approx(15)


def test_physics_does_not_move_without_keys(app):
    app.keys = FakeKeys()
    app.dt = 1000
    before = (app.camera_model.x, app.camera_model.y, app.camera_model.distance)

    app.update_physics()

    assert (app.camera_model.x, app.camera_model.y, app.camera_model.distance) == before


def test_physics_scales_in_and_out(app):
    app.dt = 1000
    app.camera_model.distance = 10
    app.keys = FakeKeys([pygame.K_e])
    app.update_physics()
    assert app.camera_model.distance > 10

    app.camera_model.distance = 10
    app.keys = FakeKeys([pygame.K_q])
    app.update_physics()
    assert app.camera_model.distance < 10


def test_update_runs_all_blocks(app):
    app.dt = 1000
    app.keys = FakeKeys()

    app.update()

    assert app.mouse_pos is not None
