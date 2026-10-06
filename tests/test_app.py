import pygame
import pytest

from scripts.app import App
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldModel, FieldView
from scripts.UI.button import Button
from scripts.UI.text import TextView
from scripts.UI.ui import UI


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


def test_app_wires_a_ui_manager(app):
    assert isinstance(app.ui, UI)


def test_app_wires_a_button(app):
    assert isinstance(app.button, Button)
    assert isinstance(app.button.text_view, TextView)
    assert app.button in app.ui.elements


def test_app_wires_a_fps_text(app):
    assert isinstance(app.fps_text, TextView)
    assert app.fps_text in app.ui.elements


def test_render_reuses_the_same_fps_text(app):
    before = app.fps_text

    app.render()
    app.render()

    assert app.fps_text is before
    assert app.fps_text.text_surface.get_width() > 0


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


def test_button_click_resets_camera(app):
    app.keys = FakeKeys()
    app.camera_model.x = 5
    app.camera_model.y = -3
    app.camera_model.distance = 100
    app.button.clicked = True

    app.update_physics()

    assert (app.camera_model.x, app.camera_model.y, app.camera_model.distance) == (0, 0, 10)


def test_update_does_not_reset_camera_without_click(app):
    app.dt = 1000
    app.keys = FakeKeys()
    app.camera_model.x = 5
    app.camera_model.y = 5
    app.camera_model.distance = 100

    app.update()

    assert (app.camera_model.x, app.camera_model.y, app.camera_model.distance) == (5, 5, 100)


def test_click_is_handled_once_and_cleared_automatically(app):
    app.camera_model.x = 5
    app.button.clicked = True

    app.update()
    assert app.camera_model.x == 0
    assert not app.button.clicked

    app.camera_model.x = 7
    app.update()
    assert app.camera_model.x == 7
