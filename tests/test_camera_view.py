import pytest

from scripts.camera import CameraModel, CameraView
from scripts.UI.text import TextView


@pytest.fixture
def view():
    return CameraView(CameraModel(x=0, y=0, distance=10, resolution=(1000, 500)))


def test_get_scale_value_returns_nice_digit(view):
    assert view.get_scale_value() in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)


def test_get_scale_value_grows_with_distance():
    near = CameraView(CameraModel(0, 0, 10, (1000, 500)))
    far = CameraView(CameraModel(0, 0, 100, (1000, 500)))

    assert far.get_scale_value() > near.get_scale_value()


def test_get_scale_value_is_based_on_first_digital():
    custom = CameraView(CameraModel(0, 0, 10, (1000, 500)))

    assert custom.get_scale_value(first_digital=(3, 7)) in (3, 7, 30, 70, 300, 700)


def test_draw_map_scale_runs_on_screen(view, screen):
    TextView.fonts = {}

    view.draw_map_scale(screen, offset=(140, 15))

    assert TextView.fonts


def test_draw_map_scale_uses_kilometers_label(screen):
    view = CameraView(CameraModel(0, 0, 100000, (1000, 500)))
    TextView.fonts = {}

    view.draw_map_scale(screen, offset=(140, 15))

    assert any(font is not None for font in TextView.fonts.values())


def test_draw_map_scale_does_not_mutate_model(view, screen):
    before = (view.model.x, view.model.y, view.model.distance)

    view.draw_map_scale(screen, offset=(140, 15))

    assert (view.model.x, view.model.y, view.model.distance) == before
