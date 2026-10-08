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


def test_colors_are_rgb_tuples():
    for color in s.COLORS.values():
        assert len(color) == 3
        assert all(0 <= channel <= 255 for channel in color)


def test_camera_defaults_exist():
    assert isinstance(s.CAMERA_START_X, (int, float))
    assert isinstance(s.CAMERA_START_Y, (int, float))
    assert s.CAMERA_START_DISTANCE > 0
    assert s.CAMERA_MOVE_SPEED > 0
    assert s.CAMERA_ZOOM_SPEED > 0


def test_scale_settings_are_consistent():
    assert s.SCALE_MIN_PIXELS < s.SCALE_MAX_PIXELS
    assert len(s.SCALE_OFFSET) == 2
    assert len(s.SCALE_LABEL_OFFSET) == 2
    assert s.SCALE_FIRST_DIGITAL


def test_hud_settings_exist():
    assert s.HUD_FONT_SIZE > 0
    assert len(s.HUD_SCALE_OFFSET) == 2
    assert len(s.HUD_FPS_MARGIN) == 2


def test_ui_example_settings_exist():
    assert s.UI_FONT_SIZE > 0
    assert len(s.UI_BUTTON_POS) == 2
    assert len(s.UI_BUTTON_SIZE) == 2
    assert len(s.UI_INPUT_POS) == 2
    assert len(s.UI_INPUT_SIZE) == 2
    assert isinstance(s.UI_INPUT_PLACEHOLDER, str)
    assert s.UI_INPUT_PLACEHOLDER
    assert len(s.UI_NAME_TEXT_POS) == 2


def test_net_settings_exist():
    assert isinstance(s.NET_HOST, str)
    assert s.NET_HOST
    assert 0 < s.NET_PORT < 65536
    assert s.NET_BUFFER_SIZE > 0
