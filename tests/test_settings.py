import scripts.settings as s


def test_size_is_width_height_pair():
    assert len(s.SIZE) == 2
    assert all(isinstance(value, int) for value in s.SIZE)


def test_fps_is_non_negative():
    assert s.FPS >= 0


def test_background_color_exists_and_is_rgb():
    assert "background" in s.COLORS
    assert len(s.COLORS["background"]) == 3


def test_name_is_a_non_empty_string():
    assert isinstance(s.NAME, str)
    assert s.NAME
